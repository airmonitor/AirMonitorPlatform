import json
import os

import requests

from lib.airmonitor_common_libs import _send_data_to_api, logger_initialization

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
AIRLY_TOKEN = os.environ["AIRLY_TOKEN"]
MEASUREMENT_LIST = []


def get_stations(lat, lng, max_distance_km):
    api_url = (
        f"https://airapi.airly.eu/v2/installations/nearest?"
        f"lat={lat}&lng={lng}&maxDistanceKM={max_distance_km}&maxResults=-1"
    )
    headers = {"Accept": "application/json", "Accept-Language": "en", "apikey": AIRLY_TOKEN}

    stations_list = []

    try:
        result = requests.get(url=api_url, headers=headers)
        if result.status_code == 200:
            airly_all_stations = json.loads(result.content.decode("utf-8"))
            for value in airly_all_stations:
                airly_dictionary = {
                    "airly_station_id": value.get("id"),
                    "airly_station_latitude": value.get("location").get("latitude"),
                    "airly_station_longitude": value.get("location").get("longitude"),
                }
                stations_list.append(airly_dictionary)
        return stations_list
    except ConnectionError as error:
        LOGGER.error("Can't get stations from airly %s", error)
        raise


def get_measurements(stations_list):
    for station in stations_list:
        station_id = station.get("airly_station_id")
        api_url = f"https://airapi.airly.eu/v2/measurements/installation?installationId={station_id}"
        headers = {"Accept": "application/json", "Accept-Language": "en", "apikey": AIRLY_TOKEN}

        try:
            result = requests.get(url=api_url, headers=headers)
            measurement = json.loads(result.content.decode("utf-8"))
            if result.status_code == 200:

                values = measurement.get("current").get("values")
                for _ in values:
                    parameter_name = _.get("name")
                    parameter_value = str(float("%.1f" % _.get("value")))
                    data = {
                        "lat": str(station.get("airly_station_latitude")),
                        "long": str(station.get("airly_station_longitude")),
                        parameter_name.lower(): parameter_value,
                        "sensor": "airly",
                    }
                    LOGGER.debug("data %s", data)
                    MEASUREMENT_LIST.append(data)

        except ConnectionError as error:
            LOGGER.error("Can't get measurements from airly %s", error)
            raise


if __name__ == "__main__":
    all_stations = get_stations(
        lat=float(os.environ["AIRLY_LAT"]),
        lng=float(os.environ["AIRLY_LONG"]),
        max_distance_km=int(os.environ["AIRLY_MAX_DISTANCE"])
    )
    LOGGER.info("all_stations %s", all_stations)
    get_measurements(stations_list=all_stations)
    airmonitor_api = _send_data_to_api(MEASUREMENT_LIST)
    LOGGER.info("measurement list %s", MEASUREMENT_LIST)
    LOGGER.info("api status code %s", airmonitor_api)
