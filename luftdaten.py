import json
import os
import urllib

import urllib3

from lib.airmonitor_common_libs import _send_data_to_api, get_content, logger_initialization

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]


def all_data():
    api_content = get_content(url="https://api.luftdaten.info/v1/filter/country=PL")
    luftdaten_all_stations = json.loads(api_content)
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

            LOGGER.debug("Sensor name: %s, Lat: %s, Long: %s", sensor_name, sensor_lat, sensor_long)

            for _ in data["sensordatavalues"]:
                value_type = _.get("value_type")
                if value_type == "P1":
                    pm10_value = _.get("value")
                    LOGGER.debug(
                        "PM10: %s, Sensor name: %s, Lat: %s, Long: %s", pm10_value, sensor_name, sensor_lat, sensor_long
                    )

                elif value_type == "P2":
                    pm25_value = _.get("value")
                    LOGGER.debug(
                        "PM25: %s, Sensor name: %s, Lat: %s, Long: %s", pm25_value, sensor_name, sensor_lat, sensor_long
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

    LOGGER.debug("final_list_of_measurements_in_dictionary %s", final_list_of_measurements_in_dictionary)

    _send_data_to_api(final_list_of_measurements_in_dictionary)


if __name__ == "__main__":
    luftdaten(event="", context="")
