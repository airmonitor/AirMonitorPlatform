# coding=utf-8

import os

from gios import all_data
import htmlmin
from lib.html_templates import HtmlTemplates
import urllib3

from lib.airmonitor_common_libs import logger_initialization
from lib.points_value import map_pins, pins, points_value
from lib.query import query

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]


def loop_gios(CZAS):
    all_values = set()

    gios_all_stations = all_data()

    result_ids = [ids["id"] for ids in gios_all_stations]
    LOGGER.debug("result_ids merged %s", result_ids)

    result_latitude = [latitude["gegrLat"] for latitude in gios_all_stations]
    LOGGER.debug("result_latitude %s", result_latitude)

    result_longitude = [longitude["gegrLon"] for longitude in gios_all_stations]
    LOGGER.debug("result_longitude %s", result_longitude)

    merged_ids_lat_long = list(zip(result_ids, result_latitude, result_longitude))
    LOGGER.debug("merged_ids_lat_long %s", merged_ids_lat_long)

    for row in merged_ids_lat_long:
        lat = row[1]
        long = row[2]
        LOGGER.debug("lat %s", lat)
        LOGGER.debug("long %s", long)

        pm10_points_value = query("pm10", lat, long)
        pm25_points_value = query("pm25", lat, long)
        pm10_points_value = points_value(pm10_points_value)
        pm25_points_value = points_value(pm25_points_value)

        LOGGER.debug("PM10 points value %s", pm10_points_value)
        LOGGER.debug("PM25 points value %s", pm25_points_value)

        try:
            float(pm10_points_value) != 0.0
            float(pm10_points_value) != 0.00
        except:
            pm10_points_value = 0.0

        try:
            float(pm25_points_value) != 0.0
            float(pm25_points_value) != 0.00
        except:
            pm25_points_value = 0.0

        if float(pm10_points_value) > 0.0 and float(pm25_points_value) == 0.0:
            returned_value_pm10 = (pm10_points_value, (float(pm10_points_value) * 2))
            LOGGER.debug("Returned value GIOS PM10 %s", returned_value_pm10)

            try:
                font_colour_icon_pm10 = pins(returned_value_pm10[1])
            except:
                font_colour_icon_pm10 = 0

            LOGGER.debug("GIOS font_colour_PM10 %s", font_colour_icon_pm10)

            map_icon_colour = map_pins(returned_value_pm10[0], returned_value_pm10[1])

            icon = map_icon_colour[0]
            icon_colour = map_icon_colour[1]

            LOGGER.debug("map_icon_colour %s", map_icon_colour)
            LOGGER.debug("icon %s", icon)
            LOGGER.debug("icon_colour %s", icon_colour)

            html_gios_pm10 = HtmlTemplates.airmonitor_sensors_html_out(
                CZAS=CZAS,
                font_colour_pm10=font_colour_icon_pm10[0],
                lat=lat,
                long=long,
                pm10_points_percentage=returned_value_pm10[1],
                returned_value_from_custom_sensors_pm10=returned_value_pm10[0],
                particle_sensor="WIOS",
            )

            html_gios = htmlmin.minify(
                html_gios_pm10, remove_comments=True, remove_empty_space=True
            )

            single_values = (lat, long, icon, icon_colour, html_gios)
            all_values.add(single_values)

        elif float(pm10_points_value) > 0.0 and float(pm25_points_value) > 0.0:

            returned_value_pm10_pm25 = (
                pm10_points_value,
                (float(pm10_points_value) * 2),
                pm25_points_value,
                (float(pm25_points_value) * 4),
            )

            LOGGER.debug("Returned value WIOS PM2.5, PM10 %s", returned_value_pm10_pm25)

            font_colour_icon_pm10 = pins(returned_value_pm10_pm25[1])
            LOGGER.debug("font_colour_icon_pm10 %s", font_colour_icon_pm10)

            font_colour_icon_pm25 = pins(returned_value_pm10_pm25[3])
            LOGGER.debug("font_colour_icon_pm25 %s", font_colour_icon_pm25)

            map_icon_colour = map_pins(
                returned_value_pm10_pm25[1], returned_value_pm10_pm25[3]
            )
            LOGGER.debug("map_icon_colour %s", map_icon_colour)

            icon = map_icon_colour[0]
            LOGGER.debug("icon %s", icon)

            icon_colour = map_icon_colour[1]
            LOGGER.debug("icon_colour %s", icon_colour)

            html_gios_pm10_pm25 = HtmlTemplates.airmonitor_sensors_html_out(
                CZAS=CZAS,
                font_colour_pm10=font_colour_icon_pm10[0],
                font_colour_pm25=font_colour_icon_pm25[0],
                lat=lat,
                long=long,
                pm10_points_percentage=returned_value_pm10_pm25[1],
                returned_value_from_custom_sensors_pm10=returned_value_pm10_pm25[0],
                pm25_points_percentage=returned_value_pm10_pm25[3],
                returned_value_from_custom_sensors_pm25=returned_value_pm10_pm25[2],
                particle_sensor="WIOS",
            )

            html_gios = htmlmin.minify(
                html_gios_pm10_pm25, remove_comments=True, remove_empty_space=True
            )
            single_values = (lat, long, icon, icon_colour, html_gios)
            all_values.add(single_values)

    return all_values


if __name__ == "__main__":
    import pytz
    import datetime

    TZ = pytz.timezone("Europe/Warsaw")
    CZAS = datetime.datetime.now(TZ).strftime("%H:%M")
    print(loop_gios(CZAS=CZAS))
