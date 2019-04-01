# coding=utf-8

import json
import os
import urllib
from urllib.request import Request

import htmlmin
from lib.html_templates import HtmlTemplates
import urllib3

from lib.airmonitor_common_libs import logger_initialization
from lib.points_value import map_pins, pins, points_value
from lib.query import query

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
LOOK_TOKEN = os.environ["LOOK_TOKEN"]


def all_data():
    url = f"http://api.looko2.com/?method=GetAll&token={LOOK_TOKEN}"

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


def loop_looko2(czas):
    all_values = set()

    try:
        looko2_all_stations = all_data()

        if looko2_all_stations != 0:
            result_ids_looko2 = [ids["Device"] for ids in looko2_all_stations]
            LOGGER.debug("result_ids_looko2 %s", result_ids_looko2)

            result_latitude_looko2 = [
                latitude["Lat"] for latitude in looko2_all_stations
            ]
            LOGGER.debug("result_latitude_looko2 %s", result_latitude_looko2)

            result_longitude_looko2 = [
                longitude["Lon"] for longitude in looko2_all_stations
            ]
            LOGGER.debug("result_longitude_looko2 %s", result_longitude_looko2)

            merged_ids_lat_long_looko2 = list(
                zip(result_ids_looko2, result_latitude_looko2, result_longitude_looko2)
            )
            LOGGER.debug("merged_ids_lat_long_looko2 %s", merged_ids_lat_long_looko2)

            for row_looko2 in merged_ids_lat_long_looko2:
                lat = row_looko2[1]
                long = row_looko2[2]

                try:
                    pm10_points_value_looko2 = query("pm10", lat, long)
                    pm10_points_value_looko2 = points_value(pm10_points_value_looko2)

                    if (
                            pm10_points_value_looko2 != 0
                            and pm10_points_value_looko2 != "Brak danych"
                    ):
                        LOGGER.debug("Look02 PM10 %s", pm10_points_value_looko2)
                        pass

                    pm25_points_value_looko2 = query("pm25", lat, long)
                    pm25_points_value_looko2 = points_value(pm25_points_value_looko2)
                    if (
                            pm25_points_value_looko2 != 0
                            and pm25_points_value_looko2 != "Brak danych"
                    ):
                        LOGGER.debug("Look02 PM25 %s", pm25_points_value_looko2)
                        pass

                    pm1_points_value_looko2 = query("pm1", lat, long)
                    pm1_points_value_looko2 = points_value(pm1_points_value_looko2)
                    if (
                            pm1_points_value_looko2 != 0
                            and pm1_points_value_looko2 != "Brak danych"
                    ):
                        LOGGER.debug("Look02 PM1 %s", pm1_points_value_looko2)
                        pass

                    returned_value_from_custom_sensors_pm10_looko2 = float(
                        pm10_points_value_looko2
                    )
                    pm10_points_percentage_looko2 = float(pm10_points_value_looko2) * 2
                    returned_value_from_custom_sensors_pm25_looko2 = float(
                        pm25_points_value_looko2
                    )
                    pm25_points_percentage_looko2 = float(pm25_points_value_looko2) * 4
                    returned_value_from_custom_sensors_pm1_looko2 = float(
                        pm1_points_value_looko2
                    )

                    if (returned_value_from_custom_sensors_pm10_looko2 != 0) or (
                            returned_value_from_custom_sensors_pm25_looko2 != 0
                    ):
                        LOGGER.debug(
                            "Look02 Calculated values %s %s %s %s ",
                            returned_value_from_custom_sensors_pm10_looko2,
                            pm10_points_percentage_looko2,
                            returned_value_from_custom_sensors_pm25_looko2,
                            pm25_points_percentage_looko2,
                        )

                        font_colour_pm10 = pins(pm10_points_percentage_looko2)
                        font_colour_pm25 = pins(pm25_points_percentage_looko2)
                        map_icon_colour = map_pins(
                            pm10_points_percentage_looko2, pm25_points_percentage_looko2
                        )
                        icon = map_icon_colour[0]
                        icon_colour = map_icon_colour[1]

                        font_colour_pm10 = str(font_colour_pm10[0])
                        font_colour_pm25 = str(font_colour_pm25[0])
                        lat = str(row_looko2[1])
                        long = str(row_looko2[2])
                        pm10_points_percentage = str(int(pm10_points_percentage_looko2))
                        pm10_points = str(
                            int(returned_value_from_custom_sensors_pm10_looko2)
                        )
                        pm25_points_percentage = str(int(pm25_points_percentage_looko2))
                        pm25_points = str(
                            int(returned_value_from_custom_sensors_pm25_looko2)
                        )
                        pm1_points = str(
                            int(returned_value_from_custom_sensors_pm1_looko2)
                        )

                        html_looko2 = HtmlTemplates.airmonitor_sensors_html_out(
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
                            particle_sensor="LOOK02",
                        )
                        html_looko2 = htmlmin.minify(
                            html_looko2, remove_comments=True, remove_empty_space=True
                        )

                        single_values = (lat, long, icon, icon_colour, html_looko2)
                        all_values.add(single_values)

                except ValueError:
                    pass
        else:
            pass
    except ValueError:
        pass
    return all_values


if __name__ == "__main__":
    import pytz
    import datetime

    TZ = pytz.timezone("Europe/Warsaw")
    CZAS = datetime.datetime.now(TZ).strftime("%H:%M")
    print(loop_looko2(czas=CZAS))
