import os

import htmlmin
from lib.html_templates import HtmlTemplates
from smogtok import all_data

from lib.airmonitor_common_libs import logger_initialization
from lib.points_value import map_pins, pins, points_value
from lib.query import query

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
SMOGTOK_LOGIN = os.environ["SMOGTOK_LOGIN"]
SMOGTOK_PASSWORD = os.environ["SMOGTOK_PASSWORD"]
SMOGTOK_URL = os.environ["SMOGTOK_URL"]


def loop_smogtok(czas):
    """
    Helper function to get all necessary data to create html iframe on airmonitor map for smogtok sensors.
    :param czas:
    :return:
    """
    all_values = set()

    try:
        smogtok_all_stations = all_data()
        LOGGER.debug("smogtok_all_stations %s", smogtok_all_stations)

        result_smogtok_latitude = [
            latitude["latitude"] for latitude in smogtok_all_stations
        ]
        LOGGER.debug("result_smogtok_latitude %s", result_smogtok_latitude)

        result_smogtok_longitude = [
            longitude["longitude"] for longitude in smogtok_all_stations
        ]
        LOGGER.debug("result_smogtok_longitude %s", result_smogtok_longitude)

        merged_smogtok_ids_lat_long = list(
            zip(result_smogtok_latitude, result_smogtok_longitude)
        )
        LOGGER.debug("merged_smogtok_ids_lat_long %s", merged_smogtok_ids_lat_long)

        for row_smogtok in merged_smogtok_ids_lat_long:
            lat = row_smogtok[0]
            long = row_smogtok[1]

            try:
                pm10_points_value_smogtok = query("pm10", lat, long)
                pm10_points_value_smogtok = points_value(pm10_points_value_smogtok)
                LOGGER.debug("SmogTok PM10 %s", pm10_points_value_smogtok)

                pm25_points_value_smogtok = query("pm25", lat, long)
                pm25_points_value_smogtok = points_value(pm25_points_value_smogtok)
                LOGGER.debug("SmogTok PM25 %s", pm25_points_value_smogtok)

                returned_value_from_custom_sensors_pm10_smogtok = float(
                    pm10_points_value_smogtok
                )
                pm10_points_percentage_smogtok = float(pm10_points_value_smogtok) * 2
                returned_value_from_custom_sensors_pm25_smogtok = float(
                    pm25_points_value_smogtok
                )
                pm25_points_percentage_smogtok = float(pm25_points_value_smogtok) * 4
                #
                if (returned_value_from_custom_sensors_pm10_smogtok != 0) or (
                        returned_value_from_custom_sensors_pm25_smogtok != 0
                ):
                    font_colour_pm10 = pins(pm10_points_percentage_smogtok)
                    font_colour_pm25 = pins(pm25_points_percentage_smogtok)
                    map_icon_colour = map_pins(
                        pm10_points_percentage_smogtok, pm25_points_percentage_smogtok
                    )
                    icon = map_icon_colour[0]
                    icon_colour = map_icon_colour[1]

                    font_colour_pm10 = str(font_colour_pm10[0])
                    font_colour_pm25 = str(font_colour_pm25[0])
                    pm10_points_percentage = str(int(pm10_points_percentage_smogtok))
                    pm10_points = str(
                        int(returned_value_from_custom_sensors_pm10_smogtok)
                    )
                    pm25_points_percentage = str(int(pm25_points_percentage_smogtok))
                    pm25_points = str(
                        int(returned_value_from_custom_sensors_pm25_smogtok)
                    )

                    html_smogtok = HtmlTemplates.airmonitor_sensors_html_out(
                        CZAS=czas,
                        font_colour_pm10=font_colour_pm10,
                        font_colour_pm25=font_colour_pm25,
                        lat=lat,
                        long=long,
                        pm10_points_percentage=pm10_points_percentage,
                        returned_value_from_custom_sensors_pm10=pm10_points,
                        pm25_points_percentage=pm25_points_percentage,
                        returned_value_from_custom_sensors_pm25=pm25_points,
                        particle_sensor="SMOGTOK",
                    )

                    html_smogtok = htmlmin.minify(
                        html_smogtok, remove_comments=True, remove_empty_space=True
                    )

                    single_values = (lat, long, icon, icon_colour, html_smogtok)
                    all_values.add(single_values)
            except Exception as e:
                LOGGER.exception("Smogtok first Exception %s", e)
                pass
    except Exception as e:
        LOGGER.exception("Smogtok second Exception %s", e)
        pass
    return all_values


if __name__ == "__main__":
    import pytz
    import datetime

    TZ = pytz.timezone("Europe/Warsaw")
    CZAS = datetime.datetime.now(TZ).strftime("%H:%M")
    print(loop_smogtok(czas=CZAS))
