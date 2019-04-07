import ast
import json
import os
import urllib
from urllib.request import Request

import urllib3

from lib.airmonitor_common_libs import _send_data_to_api, logger_initialization

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
AIRLY_TOKEN = os.environ["AIRLY_TOKEN"]


def all_data():
    url = (
        f"https://airapi.airly.eu/v1/sensors/current?southwestLat=52.29"
        f"&southwestLong=16.70&northeastLat=52.48&northeastLong=17.14"
    )

    if url.lower().startswith("http"):
        airly_url = Request(url)
        airly_url.add_header("Accept", "application/json")
        airly_url.add_header("apikey", AIRLY_TOKEN)
    else:
        raise ValueError from None

    with urllib.request.urlopen(airly_url, timeout=60) as resp:
        airly_all_stations = json.loads(resp.read())

    return airly_all_stations


def airly(event, context):
    lat = []
    long = []
    value_pm01 = []
    value_pm25 = []
    value_pm10 = []
    final_list_of_measurements_in_dictionary = []

    airly_all_stations = all_data()
    LOGGER.debug("airly_all_stations %s", airly_all_stations)

    result_ids = [ids["id"] for ids in airly_all_stations]
    LOGGER.debug("result_airly_ids %s", result_ids)

    result_airly_latitude = [
        latitude["location"]["latitude"] for latitude in airly_all_stations
    ]
    LOGGER.debug("result_airly_latitude %s", result_airly_latitude)

    result_airly_longitude = [
        longitude["location"]["longitude"] for longitude in airly_all_stations
    ]
    LOGGER.debug("result_airly_latitude %s", result_airly_longitude)

    merged_airly_ids_lat_long = list(
        zip(result_ids, result_airly_latitude, result_airly_longitude)
    )
    LOGGER.debug("merged_airly_ids_lat_long %s", merged_airly_ids_lat_long)

    for values in merged_airly_ids_lat_long:
        sensor_id = values[0]
        sensor_url = Request(
            f"https://airapi.airly.eu/v1/sensor/measurements?sensorId={sensor_id}"
        )
        sensor_url.add_header("Accept", "application/json")
        sensor_url.add_header("apikey", AIRLY_TOKEN)
        airly_sensor_data = urllib.request.urlopen(sensor_url)
        try:
            airly_sensor_data = json.loads(airly_sensor_data.read())
        except TypeError:
            airly_sensor_data = ast.literal_eval(airly_sensor_data)
        except (ValueError, IndexError, KeyError):
            airly_sensor_data = 0

        try:
            airly_sensor_data_pm1 = airly_sensor_data["currentMeasurements"]["pm1"]
            LOGGER.debug("airly_sensor_data_pm1 %s", airly_sensor_data_pm1)
        except (ValueError, IndexError, KeyError):
            airly_sensor_data_pm1 = 0

        try:
            airly_sensor_data_pm25 = airly_sensor_data["currentMeasurements"]["pm25"]
            LOGGER.debug("airly_sensor_data_pm25 %s", airly_sensor_data_pm25)
        except (ValueError, IndexError, KeyError, TypeError):
            airly_sensor_data_pm25 = 0

        try:
            airly_sensor_data_pm10 = airly_sensor_data["currentMeasurements"]["pm10"]
            LOGGER.debug("airly_sensor_data_pm10 %s", airly_sensor_data_pm10)
        except (ValueError, IndexError, KeyError, TypeError):
            airly_sensor_data_pm10 = 0

        lat.append(values[1])
        long.append(values[2])
        value_pm01.append(float(airly_sensor_data_pm1))
        value_pm25.append(float(airly_sensor_data_pm25))
        value_pm10.append(float(airly_sensor_data_pm10))

    all_entries_for_json_upload = list(
        zip(lat, long, value_pm25, value_pm10, value_pm01)
    )
    LOGGER.debug("all_entries_for_json_upload %s", all_entries_for_json_upload)

    for _ in all_entries_for_json_upload:
        data = {
            "lat": str(_[0]),
            "long": str(_[1]),
            "pm1": str(float("%.2f" % _[4])),
            "pm25": str(float("%.2f" % _[2])),
            "pm10": str(float("%.2f" % _[3])),
            "sensor": "airly",
        }
        LOGGER.debug("data %s", data)

        final_list_of_measurements_in_dictionary.append(data)

    _send_data_to_api(final_list_of_measurements_in_dictionary)


if __name__ == "__main__":
    airly("", "")
