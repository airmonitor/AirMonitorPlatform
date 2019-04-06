# coding=utf-8

import htmlmin
from lib.html_templates import HtmlTemplates
from luftdaten import all_data
import urllib3

from lib.airmonitor_common_libs import logger_initialization
from lib.points_value import map_pins, pins, points_value
from lib.query import query

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
LOGGER = logger_initialization()


def loop_luftdaten(CZAS):
    all_values = set()
    try:
        sensor_lat_list = []
        sensor_long_list = []
        luftdaten_all_data = all_data()

        for data in luftdaten_all_data:
            sensor_name = data["sensor"]["sensor_type"]["name"]

            if sensor_name == "SDS011":
                sensor_lat = data["location"]["latitude"]
                while sensor_lat[-1] == "0":
                    sensor_lat = sensor_lat[:-1]
                sensor_lat_list.append(sensor_lat)

                sensor_long = data["location"]["longitude"]
                while sensor_long[-1] == "0":
                    sensor_long = sensor_long[:-1]
                sensor_long_list.append(sensor_long)

        merged_ids_lat_long_luftdaten = list(zip(sensor_lat_list, sensor_long_list))

        LOGGER.debug("luftdaten merged lat, long %s", merged_ids_lat_long_luftdaten)

        for row_luftdaten in merged_ids_lat_long_luftdaten:
            pm10_points_value_luftdaten = query(
                "pm10", row_luftdaten[0], row_luftdaten[1]
            )
            pm10_points_value_luftdaten = points_value(pm10_points_value_luftdaten)

            try:
                if float(pm10_points_value_luftdaten) != 0:
                    LOGGER.debug("luftdaten PM10: %s", pm10_points_value_luftdaten)
                    pass
                pm25_points_value_luftdaten = query(
                    "pm25", row_luftdaten[0], row_luftdaten[1]
                )
                pm25_points_value_luftdaten = points_value(pm25_points_value_luftdaten)

                if float(pm25_points_value_luftdaten) != 0:
                    LOGGER.debug("luftdaten PM25: %s", pm25_points_value_luftdaten)
                    pass

                returned_value_from_pm10_luftdaten = float(pm10_points_value_luftdaten)
                pm10_points_percentage_luftdaten = (
                        float(pm10_points_value_luftdaten) * 2
                )

                returned_value_from_pm25_luftdaten = float(pm25_points_value_luftdaten)
                pm25_points_percentage_luftdaten = (
                        float(pm25_points_value_luftdaten) * 4
                )

                if (returned_value_from_pm10_luftdaten != 0) or (
                        returned_value_from_pm25_luftdaten != 0
                ):
                    LOGGER.debug(
                        "luftdaten calculated values, "
                        "Returned value from sensors: %s, "
                        "PM10 points percentage %s, "
                        "Returned value from PM2.5: %s, "
                        "PM2.5 points percentage %s",
                        returned_value_from_pm10_luftdaten,
                        pm10_points_percentage_luftdaten,
                        returned_value_from_pm25_luftdaten,
                        pm25_points_percentage_luftdaten,
                    )

                    font_colour_pm10 = pins(pm10_points_percentage_luftdaten)
                    font_colour_pm25 = pins(pm25_points_percentage_luftdaten)
                    LOGGER.debug(
                        "font_colour_pm10: %s, font_colour_pm25 %s",
                        font_colour_pm10,
                        font_colour_pm25,
                    )

                    map_icon_colour = map_pins(
                        pm10_points_percentage_luftdaten,
                        pm25_points_percentage_luftdaten,
                    )
                    icon = map_icon_colour[0]
                    icon_colour = map_icon_colour[1]
                    LOGGER.debug("icon: %s, icon_colour %s", icon, icon_colour)

                    font_colour_pm10 = str(font_colour_pm10[0])
                    font_colour_pm25 = str(font_colour_pm25[0])

                    lat = str(row_luftdaten[0])
                    long = str(row_luftdaten[1])
                    pm10_points_percentage = str(pm10_points_percentage_luftdaten)
                    pm10_points = str(returned_value_from_pm10_luftdaten)
                    pm25_points_percentage = str(pm25_points_percentage_luftdaten)
                    pm25_points = str(returned_value_from_pm25_luftdaten)

                    html_luftdaten = HtmlTemplates.airmonitor_sensors_html_out(
                        CZAS=CZAS,
                        font_colour_pm10=font_colour_pm10,
                        font_colour_pm25=font_colour_pm25,
                        lat=lat,
                        long=long,
                        pm10_points_percentage=pm10_points_percentage,
                        returned_value_from_custom_sensors_pm10=pm10_points,
                        pm25_points_percentage=pm25_points_percentage,
                        returned_value_from_custom_sensors_pm25=pm25_points,
                        particle_sensor="SDS011",
                    )
                    html_luftdaten = htmlmin.minify(
                        html_luftdaten, remove_comments=True, remove_empty_space=True
                    )

                    single_values = (lat, long, icon, icon_colour, html_luftdaten)

                    all_values.add(single_values)

            except ValueError:
                pass
    except:
        pass
    return all_values


if __name__ == "__main__":
    import pytz
    import datetime

    TZ = pytz.timezone("Europe/Warsaw")
    CZAS = datetime.datetime.now(TZ).strftime("%H:%M")
    print(loop_luftdaten(CZAS=CZAS))
