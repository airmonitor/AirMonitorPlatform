# coding=utf-8

import os

import htmlmin
import urllib3

from lib.airmonitor_common_libs import _data_from_google_docs, logger_initialization
from lib.html_templates import HtmlTemplates
from lib.points_value import map_pins, pins, points_value
from lib.query import query

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]


def loop_air_monitor_community(CZAS):
    all_values = set()
    returned_value_from_custom_sensors_pm10_custom_senors_pm_only = "Brak danych"
    returned_value_from_custom_sensors_pm25_custom_senors_pm_only = "Brak danych"
    returned_value_from_custom_sensors_pm1_custom_senors_pm_only = "Brak danych"

    merged_values_from_gdocs = _data_from_google_docs()
    LOGGER.debug("merged_values_from_gdocs %s", merged_values_from_gdocs)

    for row_custom_senors_pm_only in merged_values_from_gdocs:
        lat = row_custom_senors_pm_only[0]
        long = row_custom_senors_pm_only[1]

        try:
            pm10_points_value_custom_senors_pm_only = query("pm10", lat, long)
            pm10_points_value_custom_senors_pm_only = points_value(
                pm10_points_value_custom_senors_pm_only
            )
            LOGGER.debug("PM10: %s", pm10_points_value_custom_senors_pm_only)

            pm25_points_value_custom_senors_pm_only = query("pm25", lat, long)
            pm25_points_value_custom_senors_pm_only = points_value(
                pm25_points_value_custom_senors_pm_only
            )
            LOGGER.debug("PM25: %s", pm25_points_value_custom_senors_pm_only)

            pm1_points_value_custom_senors_pm_only = query("pm1", lat, long)
            pm1_points_value_custom_senors_pm_only = points_value(
                pm1_points_value_custom_senors_pm_only
            )
            LOGGER.debug("PM1: %s", pm1_points_value_custom_senors_pm_only)

            temperature_points_value = query("temperature", lat, long)
            temperature_points_value = points_value(temperature_points_value)
            LOGGER.debug("TEMPERATURE: %s", temperature_points_value)

            humidity_points_value = query("humidity", lat, long)
            humidity_points_value = points_value(humidity_points_value)
            LOGGER.debug("HUMIDITY: %s", humidity_points_value)

            pressure_points_value = query("pressure", lat, long)
            pressure_points_value = points_value(pressure_points_value)
            LOGGER.debug("PRESSURE: %s", pressure_points_value)

            co2_points_value = query("co2", lat, long)
            co2_points_value = points_value(co2_points_value)
            LOGGER.debug("CO2: %s", co2_points_value)

            tvoc_points_value = query("tvoc", lat, long)
            tvoc_points_value = points_value(tvoc_points_value)
            LOGGER.debug("TVOC: %s", tvoc_points_value)

            if pm10_points_value_custom_senors_pm_only != ("Brak danych" or None):
                returned_value_from_custom_sensors_pm10_custom_senors_pm_only = float(
                    pm10_points_value_custom_senors_pm_only
                )
                pm10_points_percentage_custom_senors_pm_only = (
                        float(pm10_points_value_custom_senors_pm_only) * 2
                )
                font_colour_pm10 = pins(pm10_points_percentage_custom_senors_pm_only)

                LOGGER.debug(
                    "pm10_points_percentage_custom_senors_pm_only: %s",
                    pm10_points_percentage_custom_senors_pm_only,
                )
                LOGGER.debug("font_colour_pm10: %s", font_colour_pm10)
                LOGGER.debug(
                    "returned_value_from_custom_sensors_pm10_custom_senors_pm_only: %s",
                    returned_value_from_custom_sensors_pm10_custom_senors_pm_only,
                )

            if pm25_points_value_custom_senors_pm_only != ("Brak danych" or None):
                returned_value_from_custom_sensors_pm25_custom_senors_pm_only = float(
                    pm25_points_value_custom_senors_pm_only
                )
                pm25_points_percentage_custom_senors_pm_only = (
                        float(pm25_points_value_custom_senors_pm_only) * 4
                )
                font_colour_pm25 = pins(pm25_points_percentage_custom_senors_pm_only)

                LOGGER.debug(
                    "pm25_points_percentage_custom_senors_pm_only: %s",
                    pm25_points_percentage_custom_senors_pm_only,
                )
                LOGGER.debug("font_colour_pm25: %s", font_colour_pm25)
                LOGGER.debug(
                    "returned_value_from_custom_sensors_pm25_custom_senors_pm_only: %s",
                    returned_value_from_custom_sensors_pm25_custom_senors_pm_only,
                )

            if pm1_points_value_custom_senors_pm_only != ("Brak danych" or None):
                returned_value_from_custom_sensors_pm1_custom_senors_pm_only = float(
                    pm1_points_value_custom_senors_pm_only
                )

                LOGGER.debug(
                    "pm1_points_value_custom_senors_pm_only: %s",
                    pm1_points_value_custom_senors_pm_only,
                )
                LOGGER.debug(
                    "returned_value_from_custom_sensors_pm1_custom_senors_pm_only: %s",
                    returned_value_from_custom_sensors_pm1_custom_senors_pm_only,
                )

            if (
                    pm10_points_value_custom_senors_pm_only != "Brak danych"
                    and pm25_points_value_custom_senors_pm_only != "Brak danych"
            ):
                map_icon_colour = map_pins(
                    pm10_points_percentage_custom_senors_pm_only,
                    pm25_points_percentage_custom_senors_pm_only,
                )
                icon = map_icon_colour[0]
                icon_colour = map_icon_colour[1]

            try:
                if (
                        returned_value_from_custom_sensors_pm10_custom_senors_pm_only != 0
                        and pm10_points_value_custom_senors_pm_only != "Brak danych"
                        and pm25_points_value_custom_senors_pm_only != "Brak danych"
                ):
                    html_airmonitor_community = HtmlTemplates.airmonitor_sensors_html_out(
                        CZAS=CZAS,
                        particle_sensor=row_custom_senors_pm_only[2],
                        font_colour_pm10=font_colour_pm10[0],
                        font_colour_pm25=font_colour_pm25[0],
                        lat=lat,
                        long=long,
                        returned_value_from_custom_sensors_pm10=returned_value_from_custom_sensors_pm10_custom_senors_pm_only,
                        pm10_points_percentage=pm10_points_percentage_custom_senors_pm_only,
                        returned_value_from_custom_sensors_pm25=returned_value_from_custom_sensors_pm25_custom_senors_pm_only,
                        pm25_points_percentage=pm25_points_percentage_custom_senors_pm_only,
                        returned_value_from_custom_sensors_pm1=returned_value_from_custom_sensors_pm1_custom_senors_pm_only,
                        temperature_points_value=temperature_points_value,
                        humidity_points_value=humidity_points_value,
                        pressure_points_value=pressure_points_value,
                        temperature_sensor="BME280",
                        co2_points_value=co2_points_value,
                        tvoc_points_value=tvoc_points_value,
                        co2_sensor="CCS811",
                        tvoc_sensor="CCS811",
                    )

                    html_airmonitor_community = htmlmin.minify(
                        html_airmonitor_community,
                        remove_comments=True,
                        remove_empty_space=True,
                    )

                    single_values = (
                        lat,
                        long,
                        icon,
                        icon_colour,
                        html_airmonitor_community,
                    )
                    all_values.add(single_values)
            except (ValueError, UnboundLocalError):
                raise
        except:
            raise
    return all_values


if __name__ == "__main__":
    import pytz
    import datetime

    TZ = pytz.timezone("Europe/Warsaw")
    CZAS = datetime.datetime.now(TZ).strftime("%H:%M")
    print(loop_air_monitor_community(CZAS=CZAS))
