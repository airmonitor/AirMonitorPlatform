#!/usr/bin/env python3.6
# coding=utf-8
"""
Module to import data from loo02.pl, parser json and send it back to airmonitor API interface.
"""
import json
import os
import time

import urllib3

from lib.airmonitor_common_libs import _send_data_to_api, get_content, logger_initialization

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOOK_API = os.environ["LOOK_API"]
LOOK_TOKEN = int(os.environ["LOOK_TOKEN"])

LOG_LEVEL = os.environ["LOG_LEVEL"]
LOGGER = logger_initialization()


def all_data():
    api_content = get_content(url=f"{LOOK_API}{LOOK_TOKEN}")
    looko2_all_stations = json.loads(api_content)
    LOGGER.debug("LOOKO2 all stations %s", looko2_all_stations)
    return looko2_all_stations


def looko2(event, context):
    epoch_time = time.time()
    result_ids = []
    result_latitude = []
    result_longitude = []
    result_epoch = []
    final_list_of_measurements_in_dictionary = []
    looko2_all_stations = all_data()

    try:
        result_ids = [ids["Device"] for ids in looko2_all_stations]
        result_latitude = [latitude["Lat"] for latitude in looko2_all_stations]
        result_longitude = [longitude["Lon"] for longitude in looko2_all_stations]
        result_epoch = [epoch["Epoch"] for epoch in looko2_all_stations]

    except KeyError:
        pass

    LOGGER.debug("result_ids %s", result_ids)
    LOGGER.debug("result_latitude %s", result_latitude)
    LOGGER.debug("result_longitude %s", result_longitude)
    LOGGER.debug("result_epoch %s", result_epoch)

    merged_ids_lat_long = list(zip(result_ids, result_latitude, result_longitude, result_epoch))

    LOGGER.debug("merged_ids_lat_long %s", merged_ids_lat_long)

    for values in merged_ids_lat_long:
        LOGGER.debug("values %s", values)

        looko2_sensor_data = get_content(
            url=f"http://api.looko2.com/?method=GetLOOKO&id={values[0]}&token={LOOK_TOKEN}"
        )
        try:
            looko2_sensor_data = json.loads(looko2_sensor_data)
        except:
            looko2_sensor_data = 0

        LOGGER.debug("looko2_sensor_data %s", looko2_sensor_data)

        if looko2_sensor_data != 0 and (55 > float(values[1]) > 47) and (epoch_time - 7200) < float(values[3]):
            try:
                looko2_sensor_data_pm1 = looko2_sensor_data["PM1"]
                LOGGER.debug("PM1:  %s", looko2_sensor_data_pm1)

            except (ValueError, KeyError, IndexError):
                looko2_sensor_data_pm1 = 0

            try:
                looko2_sensor_data_pm25 = looko2_sensor_data["PM25"]
                LOGGER.debug("PM2,5:  %s", looko2_sensor_data_pm25)

            except (ValueError, KeyError, IndexError):
                looko2_sensor_data_pm25 = 0

            try:
                looko2_sensor_data_pm10 = looko2_sensor_data["PM10"]
                LOGGER.debug("PM10:  %s", looko2_sensor_data_pm10)

            except (ValueError, KeyError, IndexError):
                looko2_sensor_data_pm10 = 0

            data = {
                "lat": str(values[1]),
                "long": str(values[2]),
                "pm1": looko2_sensor_data_pm1,
                "pm25": looko2_sensor_data_pm25,
                "pm10": looko2_sensor_data_pm10,
                "sensor": "looko2",
            }

            final_list_of_measurements_in_dictionary.append(data)

    LOGGER.debug("final_list_of_measurements_in_dictionary  %s", final_list_of_measurements_in_dictionary)

    _send_data_to_api(final_list_of_measurements_in_dictionary)
    return final_list_of_measurements_in_dictionary


if __name__ == "__main__":
    looko2("", "")
