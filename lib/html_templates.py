# coding=utf-8

import os

from lib.airmonitor_common_libs import logger_initialization

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]


class HtmlTemplates:
    @staticmethod
    def airmonitor_sensors_html_out(
            CZAS,
            font_colour_pm1="Brak danych",
            font_colour_pm10="Brak danych",
            font_colour_pm25="Brak danych",
            lat="Brak danych",
            long="Brak danych",
            returned_value_from_custom_sensors_pm10="Brak danych",
            pm10_points_percentage="Brak danych",
            returned_value_from_custom_sensors_pm25="Brak danych",
            pm25_points_percentage="Brak danych",
            returned_value_from_custom_sensors_pm1="Brak danych",
            temperature_points_value="Brak danych",
            humidity_points_value="Brak danych",
            pressure_points_value="Brak danych",
            co2_points_value="Brak danych",
            tvoc_points_value="Brak danych",
            particle_sensor="Brak danych",
            temperature_sensor="Brak danych",
            co2_sensor="Brak danych",
            tvoc_sensor="Brak danych",
    ):
        LOGGER.debug("CZAS %s", CZAS)
        LOGGER.debug("font_colour_pm1 %s", font_colour_pm1)
        LOGGER.debug("font_colour_pm10 %s", font_colour_pm10)
        LOGGER.debug("font_colour_pm25 %s", font_colour_pm25)
        LOGGER.debug("lat %s", lat)
        LOGGER.debug("long %s", long)
        LOGGER.debug("returned_value_from_custom_sensors_pm10 %s", returned_value_from_custom_sensors_pm10)
        LOGGER.debug("pm10_points_percentage %s", pm10_points_percentage)
        LOGGER.debug("returned_value_from_custom_sensors_pm25 %s", returned_value_from_custom_sensors_pm25)
        LOGGER.debug("pm25_points_percentage %s", pm25_points_percentage)
        LOGGER.debug("returned_value_from_custom_sensors_pm1 %s", returned_value_from_custom_sensors_pm1)
        LOGGER.debug("temperature_points_value %s", temperature_points_value)
        LOGGER.debug("humidity_points_value %s", humidity_points_value)
        LOGGER.debug("pressure_points_value %s", pressure_points_value)
        LOGGER.debug("co2_points_value %s", co2_points_value)
        LOGGER.debug("tvoc_points_value %s", tvoc_points_value)
        LOGGER.debug("particle_sensor %s", particle_sensor)
        LOGGER.debug("temperature_sensor %s", temperature_sensor)
        LOGGER.debug("co2_sensor %s", co2_sensor)
        LOGGER.debug("tvoc_sensor %s", tvoc_sensor)

        if particle_sensor.upper() in ("PMS7003", "PMS5003"):
            particle_sensor_link = "https://allegro.pl/kategoria/inteligentny-dom-czujniki-251245?string=pms7003&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-hou-1-2-0329"
        elif particle_sensor.upper() in ("SDS021", "SDS011", "SDSESP"):
            particle_sensor_link = "https://allegro.pl/listing?string=SDS011&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-ele-1-2-0329"
        elif particle_sensor.upper() == "WIOS":
            particle_sensor_link = "http://powietrze.gios.gov.pl/pjp/current"
        elif particle_sensor.upper() == "AIRLY":
            particle_sensor_link = "https://airly.eu/pl/"
        elif particle_sensor.upper() == "LOOK02":
            particle_sensor_link = "https://looko2.com/"
        elif particle_sensor.upper() == "SMOGTOK":
            particle_sensor_link = "https://smogtok.com/"
        else:
            particle_sensor_link = "https://allegro.pl/kategoria/inteligentny-dom-czujniki-251245?string=pms7003&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-hou-1-2-0329"

        if tvoc_points_value != "Brak danych":
            tvoc_points_value_unit = "ppb"
            tvoc_html = (
                    """<tr>
                                        <td>TVOC<br>
                                        </td>
                                        <td>
                                        <b>
                                        <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=16&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(tvoc_points_value)
                    + " "
                    + str(tvoc_points_value_unit)
                    + """</a>
                            </>
                            </td>
                            <td>
                            <a target="_blank" href="https://allegro.pl/listing?string=ccs811&order=m&bmatch=baseline-n-dict-ele-1-2-1130">"""
                    + str(tvoc_sensor)
                    + """</a>
                            </td>
                            </tr>"""
            )
        else:
            tvoc_html = ""

        if co2_points_value != "Brak danych":
            co2_points_value_unit = "ppm"
            co2_html = (
                    """<tr>
                                    <td>CO2<br>
                                    </td>
                                    <td>
                                    <b>
                                    <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=15&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(co2_points_value)
                    + " "
                    + str(co2_points_value_unit)
                    + """</a>
                        </>
                        </td>
                        <td>
                        <a target="_blank" href="https://allegro.pl/listing?string=ccs811&order=m&bmatch=baseline-n-dict-ele-1-2-1130">"""
                    + str(co2_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            co2_html = ""

        if pressure_points_value != "Brak danych":
            pressure_points_value_unit = "hPa"
            pressure_html = (
                    """<tr>
                                    <td>Ciśnienie<br>
                                    </td>
                                    <td>
                                    <b>
                                    <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=7&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(pressure_points_value)
                    + " "
                    + str(pressure_points_value_unit)
                    + """</a>
                        </b>
                        </td>
                        <td>
                        <a target="_blank" href="https://allegro.pl/listing?string=bme280&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-ele-1-2-0329">"""
                    + str(temperature_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            pressure_html = ""

        if humidity_points_value != "Brak danych":
            humidity_points_value_unit = "%"
            humidity_html = (
                    """<tr>
                                    <td>Wilgotność</td>
                                    <td>
                                    <b>
                                    <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=5&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(humidity_points_value)
                    + " "
                    + str(humidity_points_value_unit)
                    + """</a>
                        </b>
                        </td>
                        <td>
                        <a target="_blank" href="https://allegro.pl/listing?string=bme280&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-ele-1-2-0329">"""
                    + str(temperature_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            humidity_html = " "

        if temperature_points_value != "Brak danych":
            temperature_points_value_unit = "°C"
            temperature_html = (
                    """<tr>
                                    <td>Temperatura<br>
                                    </td>
                                    <td>
                                    <b>
                                    <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=5&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(temperature_points_value)
                    + " "
                    + str(temperature_points_value_unit)
                    + """</a>
                        </>
                        </td>
                        <td>
                        <a target="_blank" href="https://allegro.pl/listing?string=bme280&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-ele-1-2-0329">"""
                    + str(temperature_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            temperature_html = ""

        if pm25_points_percentage != "Brak danych":

            pm25_points_percentage_unit = "µg/m<sup>3</sup>"
            pm25_html = (
                    """<tr>
                                    <td><font color="""
                    + str(font_colour_pm25)
                    + """>
                        PM2,5
                        </font>
                        <br>
                        </td>
                        <td>
                        <font color="""
                    + str(font_colour_pm25)
                    + """>
                        <b>
                        <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=14&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(returned_value_from_custom_sensors_pm25)
                    + " "
                    + str(pm25_points_percentage_unit)
                    + """</a>
                        </b>
                        ("""
                    + str(pm25_points_percentage)
                    + """ %)
                        </font>
                        </td>
                        <td>
                        <a target="_blank" href="""
                    + str(particle_sensor_link)
                    + """>"""
                    + str(particle_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            pm25_html = " "

        if pm10_points_percentage != "Brak danych":
            pm10_points_percentage_unit = "µg/m<sup>3</sup>"
            pm10_html = (
                    """<tr>
                                    <td>
                                    <font color="""
                    + str(font_colour_pm10)
                    + """>
                        PM10
                        </font>
                        </td>
                        <td>
                        <font color="""
                    + str(font_colour_pm10)
                    + """>
                        <b>
                        <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=13&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(returned_value_from_custom_sensors_pm10)
                    + " "
                    + str(pm10_points_percentage_unit)
                    + """</a>
                        </b>
                        ("""
                    + str(pm10_points_percentage)
                    + """ %)
                        </font>
                        </td>
                        <td>
                        <a target="_blank" href="""
                    + str(particle_sensor_link)
                    + """>"""
                    + str(particle_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            pm10_html = " "

        if returned_value_from_custom_sensors_pm1 != "Brak danych" and particle_sensor.upper() != (
                "SDS021" or "SDS011" or "SDSESP"
        ):

            pm1_points_percentage_unit = "µg/m<sup>3</sup>"
            pm1_html = (
                    """<tr>
                                    <td>
                                    <font color="""
                    + str(font_colour_pm1)
                    + """>
                        PM1
                        </font>
                        </td>
                        <td>
                        <font color="""
                    + str(font_colour_pm1)
                    + """>
                        <b>
                        <a target="_blank" href="https://metrics.airmonitor.pl/dashboard/db/airmonitor?orgId=1&panelId=19&fullscreen&var-latitude="""
                    + str(lat)
                    + """&var-longitude="""
                    + str(long)
                    + """ ">  """
                    + str(returned_value_from_custom_sensors_pm1)
                    + " "
                    + str(pm1_points_percentage_unit)
                    + """</a>
                        </b>
                        ("""
                    + str(returned_value_from_custom_sensors_pm1)
                    + """ %)
                        </font>
                        </td>
                        <td>
                        <a target="_blank" href="""
                    + str(particle_sensor_link)
                    + """>"""
                    + str(particle_sensor)
                    + """</a>
                        </td>
                        </tr>
                        """
            )
        else:
            pm1_html = " "

        html = (
                """
                           <!doctype html>
                           <html>
                           <style>
                           table {
                           font-family: arial, sans-serif;
                           border-collapse: collapse;
                           width: 100%;
                           }
                           td, th {
                           border: 1px solid #dddddd;
                           text-align: left;
                           padding: 8px;
                           }
                           tr:nth-child(even) {
                           background-color: #dddddd;
                           }
                           </style>
                           <p>
                           <font face="arial">
                           <b>Czas pomiaru  """
                + str(CZAS)
                + """</b>
               </font>
               </p>
               <table>
               <tbody>
               <tr>
               <th>Parametr</th>
               <th>Wartość</th>
               <th>Sensor</th>
               </tr>
               """
                + str(pm1_html)
                + """
               """
                + str(pm25_html)
                + """
               """
                + str(pm10_html)
                + """
               """
                + str(temperature_html)
                + """
               """
                + str(humidity_html)
                + """
               """
                + str(pressure_html)
                + """
               """
                + str(co2_html)
                + """
               """
                + str(tvoc_html)
                + """
               </tbody>
               </table>
               <p>
               <font face="arial">
               Jeśli lutownica, pistolet do klejenia na gorąco nie są Tobie straszne wtenczas samodzielnie
               <a target="_blank" href="http://airmonitor.pl">możesz zbudować swoją stację</a> do pomiaru jakości 
               powietrza z podstawową funkcjonalnością.
               </font>
               <br>
               </p>
               </html>
               """
        )
        LOGGER.debug("HTML for lat, long  %s %s %s", lat, long, html)
        return html
