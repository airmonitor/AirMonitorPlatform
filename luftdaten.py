import json
import os
import urllib
from urllib.request import Request

import requests
from requests.adapters import HTTPAdapter
import urllib3
from urllib3.util import Retry

from lib.airmonitor_common_libs import _send_data_to_api, logger_initialization

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]


def _requests_retry_session(
        retries=3, back_off_factor=3, status_force_list=(500, 502, 504), session=None
):
    """
    Function will help with exponential back-off when calling BI API
    :param retries: int
    :param back_off_factor: int
    :param status_force_list: list http codes returned by api
    :param session: None
    :return: session
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=back_off_factor,
        status_forcelist=status_force_list,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def all_data():
    url = "http://api.luftdaten.info/v1/filter/country=PL"

    if url.lower().startswith("http"):
        luftdaten = Request(url)
    else:
        raise ValueError from None

    with urllib.request.urlopen(luftdaten, timeout=60) as resp:
        luftdaten_all_stations = json.loads(resp.read())

    LOGGER.debug("Luftdaten all stations %s", luftdaten_all_stations)
    for data in luftdaten_all_stations:
        yield data


def luftdaten(event, context):
    sensor_name_list = []
    sensor_lat_list = []
    sensor_long_list = []
    pm10_value = ""
    pm25_value = ""
    final_list_of_measurements_in_dictionary = []
    luftdaten_all_data = all_data()
    try:
        for data in luftdaten_all_data:
            sensor_name = data["sensor"]["sensor_type"]["name"]
            sensor_name_list.append(sensor_name)

            sensor_lat = data["location"]["latitude"]
            sensor_lat_list.append(sensor_lat)

            sensor_long = data["location"]["longitude"]
            sensor_long_list.append(sensor_long)

            LOGGER.debug(
                "Sensor name: %s, Lat: %s, Long: %s",
                sensor_name,
                sensor_lat,
                sensor_long,
            )

            for _ in data["sensordatavalues"]:
                value_type = _.get("value_type")
                if value_type == "P1":
                    pm10_value = _.get("value")
                    LOGGER.debug(
                        "PM10: %s, Sensor name: %s, Lat: %s, Long: %s",
                        pm10_value,
                        sensor_name,
                        sensor_lat,
                        sensor_long,
                    )

                elif value_type == "P2":
                    pm25_value = _.get("value")
                    LOGGER.debug(
                        "PM25: %s, Sensor name: %s, Lat: %s, Long: %s",
                        pm25_value,
                        sensor_name,
                        sensor_lat,
                        sensor_long,
                    )

            if sensor_name == "SDS011":
                data = {
                    "lat": sensor_lat,
                    "long": sensor_long,
                    "pm25": pm25_value,
                    "pm10": pm10_value,
                    "sensor": sensor_name,
                }

                LOGGER.debug("data %s", data)
                final_list_of_measurements_in_dictionary.append(data)

    except urllib.error.HTTPError as e:
        LOGGER.critical("luftdaten returned %s", e)

    LOGGER.debug(
        "final_list_of_measurements_in_dictionary %s",
        final_list_of_measurements_in_dictionary,
    )

    _send_data_to_api(final_list_of_measurements_in_dictionary)


if __name__ == "__main__":
    luftdaten(event="", context="")
