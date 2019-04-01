# coding=utf-8

import os

from airly import all_data
import htmlmin
from lib.html_templates import HtmlTemplates
import urllib3

from lib.airmonitor_common_libs import logger_initialization
from lib.points_value import map_pins, pins, points_value
from lib.query import query

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
TOKEN = os.environ['TOKEN']


def loop_airly(czas):
    all_values = set()

    try:
        airly_all_stations = all_data()
        LOGGER.debug("airly_all_stations %s", airly_all_stations)

        result_airly_latitude = [latitude['location']['latitude'] for latitude in airly_all_stations]
        LOGGER.debug("result_airly_latitude %s", result_airly_latitude)

        result_airly_longitude = [longitude['location']['longitude'] for longitude in airly_all_stations]
        LOGGER.debug("result_airly_longitude %s", result_airly_longitude)

        merged_airly_ids_lat_long = list(zip(result_airly_latitude, result_airly_longitude))
        LOGGER.debug("merged_airly_ids_lat_long %s", merged_airly_ids_lat_long)

        for row_airly in merged_airly_ids_lat_long:
            lat = row_airly[0]
            long = row_airly[1]

            try:
                pm10_points_value_airly = query("pm10", lat, long)
                pm10_points_value_airly = points_value(pm10_points_value_airly)
                LOGGER.debug("Airly PM10 %s", pm10_points_value_airly)

                pm25_points_value_airly = query("pm25", lat, long)
                pm25_points_value_airly = points_value(pm25_points_value_airly)
                LOGGER.debug("Airly PM25 %s", pm25_points_value_airly)

                ppm1_points_value_airly = query("pm1", lat, long)
                ppm1_points_value_airly = points_value(ppm1_points_value_airly)
                LOGGER.debug("Airly PM1 %s", ppm1_points_value_airly)

                returned_value_from_custom_sensors_pm10_airly = float(pm10_points_value_airly)
                pm10_points_percentage_airly = float(pm10_points_value_airly) * 2
                returned_value_from_custom_sensors_pm25_airly = float(pm25_points_value_airly)
                pm25_points_percentage_airly = float(pm25_points_value_airly) * 4
                returned_value_from_custom_sensors_pm1_airly = float(ppm1_points_value_airly)

                if (returned_value_from_custom_sensors_pm10_airly != 0) or \
                        (returned_value_from_custom_sensors_pm25_airly != 0):
                    LOGGER.debug(
                        "Airly Calculated values %s %s %s %s %s",
                        returned_value_from_custom_sensors_pm10_airly,
                        pm10_points_percentage_airly,
                        returned_value_from_custom_sensors_pm25_airly,
                        pm25_points_percentage_airly,
                        returned_value_from_custom_sensors_pm1_airly
                    )

                    font_colour_pm10 = pins(pm10_points_percentage_airly)
                    font_colour_pm25 = pins(pm25_points_percentage_airly)
                    map_icon_colour = map_pins(pm10_points_percentage_airly, pm25_points_percentage_airly)
                    icon = map_icon_colour[0]
                    icon_colour = map_icon_colour[1]

                    font_colour_pm10 = str(font_colour_pm10[0])
                    font_colour_pm25 = str(font_colour_pm25[0])
                    pm10_points_percentage = str(int(pm10_points_percentage_airly))
                    pm10_points = str(int(returned_value_from_custom_sensors_pm10_airly))
                    pm25_points_percentage = str(int(pm25_points_percentage_airly))
                    pm25_points = str(int(returned_value_from_custom_sensors_pm25_airly))
                    pm1_points = str(int(returned_value_from_custom_sensors_pm1_airly))

                    html_airly = HtmlTemplates.airmonitor_sensors_html_out(
                        CZAS=czas,
                        font_colour_pm10=font_colour_pm10,
                        font_colour_pm25=font_colour_pm25,
                        lat=lat,
                        long=long,
                        pm10_points_percentage=pm10_points_percentage,
                        returned_value_from_custom_sensors_pm10=pm10_points,
                        pm25_points_percentage=pm25_points_percentage,
                        returned_value_from_custom_sensors_pm25=pm25_points,
                        returned_value_from_custom_sensors_pm1=pm1_points,
                        particle_sensor="AIRLY")
                    html_airly = htmlmin.minify(html_airly,
                                                remove_comments=True,
                                                remove_empty_space=True)

                    single_values = (lat, long, icon, icon_colour, html_airly)
                    all_values.add(single_values)
            except ValueError:
                pass
    except KeyError:
        pass
    return all_values


if __name__ == "__main__":
    import pytz
    import datetime

    TZ = pytz.timezone('Europe/Warsaw')
    CZAS = datetime.datetime.now(TZ).strftime("%H:%M")

    print(loop_airly(czas=CZAS))
