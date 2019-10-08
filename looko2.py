#!/usr/bin/env python3.6
# coding=utf-8
"""
Module to import data from loo02.pl, parser json and send it back to airmonitor API interface.
"""
import json
import os
import time
import urllib
from urllib.request import Request

import urllib3

from lib.airmonitor_common_libs import _send_data_to_api, logger_initialization

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOOK_TOKEN = int(os.environ["LOOK_TOKEN"])

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
LOOK_API = os.environ["LOOK_API"]


def all_data():
    url = f"{LOOK_API}{LOOK_TOKEN}"

    if url.lower().startswith("http"):
        looko2 = Request(url)
    else:
        raise ValueError from None

    try:
        resp = urllib.request.urlopen(looko2, timeout=60)
        looko2_all_stations = json.loads(resp.read())
    except ValueError:
        looko2_all_stations = None

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

    lat = []
    long = []
    value_pm01 = []
    value_pm25 = []
    value_pm10 = []

    for values in merged_ids_lat_long:
        LOGGER.debug("values %s", values)

        sensor_url = Request(f"http://api.looko2.com/?method=GetLOOKO&id={values[0]}&token={LOOK_TOKEN}")

        try:
            looko2_sensor_data = urllib.request.urlopen(sensor_url)
            looko2_sensor_data = json.loads(looko2_sensor_data.read())
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

            lat.append(values[1])
            long.append(values[2])
            value_pm01.append(float(looko2_sensor_data_pm1))
            value_pm25.append(float(looko2_sensor_data_pm25))
            value_pm10.append(float(looko2_sensor_data_pm10))

    all_entries_for_json_upload = list(zip(lat, long, value_pm25, value_pm10, value_pm01))

    LOGGER.debug("all_entries_for_json_upload  %s", all_entries_for_json_upload)

    for values in all_entries_for_json_upload:
        data = {
            "lat": str(values[0]),
            "long": str(values[1]),
            "pm1": str(float("%.2f" % values[4])),
            "pm25": str(float("%.2f" % values[2])),
            "pm10": str(float("%.2f" % values[3])),
            "sensor": "looko2",
        }

        final_list_of_measurements_in_dictionary.append(data)

    _send_data_to_api(final_list_of_measurements_in_dictionary)


if __name__ == "__main__":
    looko2("", "")
