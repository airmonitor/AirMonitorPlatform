from datetime import datetime
import json
import os

import requests

from lib.airmonitor_common_libs import _send_data_to_api, logger_initialization

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
SMOGTOK_LOGIN = os.environ["SMOGTOK_LOGIN"]
SMOGTOK_PASSWORD = os.environ["SMOGTOK_PASSWORD"]
SMOGTOK_URL = os.environ["SMOGTOK_URL"]


def all_data():
    """
    Function to get json with all measurements from smogotok api using basic authentication.
    :return:
    """
    if SMOGTOK_URL.lower().startswith("http" or "https"):
        response = requests.get(
            url=SMOGTOK_URL, timeout=30, auth=requests.auth.HTTPBasicAuth(SMOGTOK_LOGIN, SMOGTOK_PASSWORD)
        )

    else:
        raise ValueError from None

    try:
        if response.status_code == 200:
            smogtok_all_stations = json.loads(response.text)
            LOGGER.debug("SMOGTOK smogtok_all_stations %s", smogtok_all_stations)
            return smogtok_all_stations
        else:
            pass
    except Exception as e:
        raise


def convert_date(measured_time):
    """
    Convert obtained from provider api date to correct for influxdb
    :param measured_time:
    :return: example - '2019-01-31T19:25:00Z'
    """
    converted_measured_time = datetime.strptime(measured_time, "%Y-%m-%d %H:%M:%S")
    return converted_measured_time.strftime("%Y-%m-%dT%H:%M:%SZ")


def smogtok(event, context):
    """
    Function to get all measurements from smogotok api and pass it to AWS Gateway.
    :param event:
    :param context:
    :return:
    """
    final_list_of_measurements_in_dictionary = []
    for entry in all_data():
        LOGGER.debug("SMOGTOK entry %s", entry)

        measurement_type = None
        measurement_value = None
        measure_time = None
        lat = entry.get("latitude")
        long = entry.get("longitude")

        for measurement in entry.get("values"):
            LOGGER.debug("SMOGTOK measurement %s", measurement)

            if measurement.get("value"):
                measurement_value = measurement.get("value")
                measure_time = convert_date(measurement.get("dt"))
                measurement_type = (
                    "pm10"
                    if measurement.get("type") == "PM10"
                    else "pm25"
                    if measurement.get("type") == "PM2.5"
                    else None
                )
            else:
                pass

            data = {
                "lat": lat,
                "long": long,
                measurement_type: measurement_value,
                "time": measure_time,
                "sensor": "smogotok",
            }

            final_list_of_measurements_in_dictionary.append(data)

        LOGGER.debug("SMOGTOK final_list_of_measurements_in_dictionary %s", final_list_of_measurements_in_dictionary)

    _send_data_to_api(final_list_of_measurements_in_dictionary)


if __name__ == "__main__":
    smogtok("", "")
