# coding=utf-8

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


def all_data():
    url = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"

    if url.lower().startswith("http"):
        gios = Request(url)
    else:
        raise ValueError from None

    with urllib.request.urlopen(gios, timeout=60) as resp:
        gios_all_stations = json.loads(resp.read())

    return gios_all_stations


def gios(event, context):
    pm25_count = 0  # How many pm2,5 metrics were found totaly
    pm10_count = 0  # How many pm10 metrics were found totaly
    pm25_missing_count = 0  # How many pm2,5 metrics were found empty
    pm10_missing_count = 0  # How many pm10 metrics were found empty
    result_ids = []
    result_latitude = []
    result_longitude = []
    lat_pm10 = []
    long_pm10 = []
    pm10 = []
    lat_pm25 = []
    long_pm25 = []
    pm25 = []
    final_list_of_measurements_in_dictionary = []

    gios_all_stations = all_data()
    LOGGER.debug("gios_all_stations %s", gios_all_stations)

    try:
        result_ids = [ids["id"] for ids in gios_all_stations]
        LOGGER.debug("result_ids %s", result_ids)

        result_latitude = [latitude["gegrLat"] for latitude in gios_all_stations]
        LOGGER.debug("result_latitude %s", result_latitude)

        result_longitude = [longitude["gegrLon"] for longitude in gios_all_stations]
        LOGGER.debug("result_longitude %s", result_longitude)

    except (KeyError, ValueError):
        LOGGER.debug("Can't read gios data")

    merged_ids_lat_long = list(zip(result_ids, result_latitude, result_longitude))

    for values in merged_ids_lat_long:
        sensor_url = Request("http://api.gios.gov.pl/pjp-api/rest/station/sensors/" + str(values[0]))
        gios_sensor_data = urllib.request.urlopen(sensor_url, timeout=60)

        try:
            gios_sensor_data = json.loads(gios_sensor_data.read())
        except TypeError:
            gios_sensor_data = ast.literal_eval(gios_sensor_data)
        except (ValueError, IndexError, KeyError, TypeError):
            gios_sensor_data = 2

        for i in range(10):
            LOGGER.debug("Trying %s", 1)

            try:

                param_formula = str(gios_sensor_data[i]["param"]["paramFormula"])
                sensor_id = gios_sensor_data[i]["id"]
                if param_formula == str("PM10"):
                    pm10_count += 1
                    LOGGER.debug("Param formula %s", param_formula)
                    station_id_data = Request(f"http://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}")
                    station_sensor_data = urllib.request.urlopen(station_id_data, timeout=60)
                    station_sensor_data = json.loads(station_sensor_data.read())
                    LOGGER.debug("Param station_sensor_data %s", station_sensor_data)

                    try:
                        pm10_value = station_sensor_data["values"][0]["value"]
                        pm10_value = float(pm10_value)
                        LOGGER.debug("PM10_value %s", pm10_value)

                    except (TypeError, IndexError):
                        pm10_missing_count += 1
                        continue

                    pm10.append(pm10_value)
                    lat_pm10.append(values[1])
                    long_pm10.append(values[2])

                    LOGGER.debug("pm10, lat_pm10, long_pm10 %s %s %s ", pm10, lat_pm10, long_pm10)

                elif str(param_formula) == str("PM2.5"):
                    pm25_count += 1
                    LOGGER.debug("Param formula %s", param_formula)

                    station_id_data = Request(f"http://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}")
                    station_sensor_data = urllib.request.urlopen(station_id_data, timeout=60)
                    station_sensor_data = json.loads(station_sensor_data.read())
                    LOGGER.debug("Param station_sensor_data %s", station_sensor_data)

                    try:
                        pm25_value = station_sensor_data["values"][0]["value"]
                        pm25_value = float(pm25_value)
                        LOGGER.debug("pm25_value %s", pm25_value)

                    except (TypeError, IndexError):
                        pm25_missing_count += 1
                        continue

                    pm25.append(pm25_value)
                    lat_pm25.append(values[1])
                    long_pm25.append(values[2])

                    LOGGER.debug("pm25, lat_pm25, long_pm25 %s %s %s ", pm25, lat_pm25, long_pm25)

            except:
                continue

    print(
        f"PM25 missing count {pm25_missing_count}\n"
        f"PM25 total count {pm25_count}\n"
        f"PM25 sum of valid measurements {pm25_count - pm25_missing_count}\n"
        f"PM10 missing count {pm10_missing_count}\n"
        f"PM10 total count {pm10_count}\n"
        f"PM10 sum of valid measurements {pm10_count - pm10_missing_count}\n"
    )

    merged_ids_lat_long_pm10 = list(zip(lat_pm10, long_pm10, pm10))
    LOGGER.debug("merged_ids_lat_long_pm10 %s ", merged_ids_lat_long_pm10)

    merged_ids_lat_long_pm25 = list(zip(lat_pm25, long_pm25, pm25))
    LOGGER.debug("merged_ids_lat_long_pm25 %s ", merged_ids_lat_long_pm25)

    for values in merged_ids_lat_long_pm10:
        data = {"lat": str(values[0]), "long": str(values[1]), "pm10": float("%.2f" % values[2]), "sensor": "WIOS"}
        LOGGER.debug("data %s", data)
        final_list_of_measurements_in_dictionary.append(data)

    for values in merged_ids_lat_long_pm25:
        data = {"lat": str(values[0]), "long": str(values[1]), "pm25": float("%.2f" % values[2]), "sensor": "WIOS"}
        LOGGER.debug("data %s", data)
        final_list_of_measurements_in_dictionary.append(data)

    LOGGER.debug("final_list_of_measurements_in_dictionary %s", final_list_of_measurements_in_dictionary)
    _send_data_to_api(final_list_of_measurements_in_dictionary)


if __name__ == "__main__":
    gios("", "")
