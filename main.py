# coding=utf-8

import datetime
import os
import platform

import branca
import folium
from folium.plugins import MarkerCluster
from folium.plugins.measure_control import MeasureControl
import pytz
import urllib3

from lib.loop_airly import loop_airly
from lib.loop_airmonitor import loop_air_monitor_community
from lib.loop_gios import loop_gios
from lib.loop_looko2 import loop_looko2
from lib.loop_luftdaten import loop_luftdaten
from lib.loop_smogtok import loop_smogtok

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# circle maker section
radius = 100
weight_value = 0

TILES = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
ATTR = (
    'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, '
    'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
)


def loop_last(event, context):
    tz = pytz.timezone("Europe/Warsaw")
    czas = datetime.datetime.now(tz).strftime("%H:%M")

    mapa = folium.Map(
        location=[52.40729, 16.93276], tiles=TILES, zoom_start=7, attr=ATTR
    )
    marker_cluster = MarkerCluster().add_to(mapa)
    measure_feature = MeasureControl()
    measure_feature.add_to(mapa)

    if os.path.exists("/tmp/index.html"):
        os.remove("/tmp/index.html")
    else:
        print("The file does not exist")

    """ Airly """
    try:
        for values in loop_airly(czas=czas):
            lat, long, icon, icon_colour, html_airly = values

            iframe = branca.element.IFrame(html=html_airly, width=430, height=330)

            popup = folium.Popup(iframe, max_width=500)

            folium.Marker(
                [float(lat), float(long)],
                icon=folium.Icon(color=icon_colour, icon=icon),
                popup=popup,
            ).add_to(marker_cluster)

            folium.Circle(
                location=[float(lat), float(long)],
                radius=radius,
                color=icon_colour,
                weight=weight_value,
                fill_opacity=0.3,
                opacity=1,
                fill_color=icon_colour,
                fill=True,  # gets overridden by fill_color
                # popup='{} meters'.format(radius),
                # tooltip='I am in meters',
            ).add_to(mapa)
    except Exception as e:
        print(f"Airly Exception {e}")
        pass

    """ Luftdaten """
    try:
        for values in loop_luftdaten(CZAS=czas):
            lat, long, icon, icon_colour, html_luftdaten = values

            iframe = branca.element.IFrame(html=html_luftdaten, width=430, height=330)

            popup = folium.Popup(iframe, max_width=500)

            folium.Marker(
                [float(lat), float(long)],
                icon=folium.Icon(color=icon_colour, icon=icon),
                popup=popup,
            ).add_to(marker_cluster)

            folium.Circle(
                location=[float(lat), float(long)],
                radius=radius,
                color=icon_colour,
                weight=weight_value,
                fill_opacity=0.3,
                opacity=1,
                fill_color=icon_colour,
                fill=True,  # gets overridden by fill_color
                # popup='{} meters'.format(radius),
                # tooltip='I am in meters',
            ).add_to(mapa)
    except Exception as e:
        print(f"Luftdaten exception {e}")

    """ GIOS """
    try:
        for values in loop_gios(CZAS=czas):
            lat, long, icon, icon_colour, html_gios = values

            iframe_pm10_pm25 = branca.element.IFrame(
                html=html_gios, width=430, height=330
            )
            popup_pm10_pm25 = folium.Popup(iframe_pm10_pm25, max_width=500)

            folium.Marker(
                [float(lat), float(long)],
                icon=folium.Icon(color=icon_colour, icon=icon),
                popup=popup_pm10_pm25,
            ).add_to(marker_cluster)

            folium.Circle(
                location=[float(lat), float(long)],
                radius=radius,
                color=icon_colour,
                weight=weight_value,
                fill_opacity=0.3,
                opacity=1,
                fill_color=icon_colour,
                fill=True,  # gets overridden by fill_color
                # popup='{} meters'.format(radius),
                # tooltip='I am in meters',
            ).add_to(mapa)
    except Exception as e:
        print(f"GIOS exception {e}")

    """ Look02 """
    try:
        for values in loop_looko2(czas=czas):
            lat, long, icon, icon_colour, html_looko2 = values
            iframe = branca.element.IFrame(html=html_looko2, width=430, height=330)
            popup = folium.Popup(iframe, max_width=500)
            folium.Marker(
                [float(lat), float(long)],
                icon=folium.Icon(color=icon_colour, icon=icon),
                popup=popup,
            ).add_to(marker_cluster)
            folium.Circle(
                location=[float(lat), float(long)],
                radius=radius,
                color=icon_colour,
                weight=weight_value,
                fill_opacity=0.3,
                opacity=1,
                fill_color=icon_colour,
                fill=True,  # gets overridden by fill_color
                # popup='{} meters'.format(radius),
                # tooltip='I am in meters',
            ).add_to(mapa)
    except Exception as e:
        print(f"LookO2 exception {e}")
    """ AIRMONITOR COMMUNITY SENSORS """
    try:
        for values in loop_air_monitor_community(CZAS=czas):
            lat, long, icon, icon_colour, html_airmonitor_community = values

            iframe = branca.element.IFrame(
                html=html_airmonitor_community, width=430, height=370
            )

            popup = folium.Popup(iframe, max_width=500)

            folium.Marker(
                [float(lat), float(long)],
                icon=folium.Icon(color=icon_colour, icon=icon),
                popup=popup,
            ).add_to(marker_cluster)

            folium.Circle(
                location=[float(lat), float(long)],
                radius=radius,
                color=icon_colour,
                weight=weight_value,
                fill_opacity=0.3,
                opacity=1,
                fill_color=icon_colour,
                fill=True,  # gets overridden by fill_color
            ).add_to(mapa)
    except Exception as e:
        print(f"AirMonitor exception {e}")

    """ SmogTok """
    try:
        for values in loop_smogtok(czas=czas):
            lat, long, icon, icon_colour, html_smogtok = values
            iframe = branca.element.IFrame(html=html_smogtok, width=430, height=330)
            popup = folium.Popup(iframe, max_width=500)
            folium.Marker(
                [float(lat), float(long)],
                icon=folium.Icon(color=icon_colour, icon=icon),
                popup=popup,
            ).add_to(marker_cluster)
            folium.Circle(
                location=[float(lat), float(long)],
                radius=radius,
                color=icon_colour,
                weight=weight_value,
                fill_opacity=0.3,
                opacity=1,
                fill_color=icon_colour,
                fill=True,  # gets overridden by fill_color
            ).add_to(mapa)
    except Exception as e:
        print(f"SmogTok exception {e}")

    folium.LatLngPopup().add_to(mapa)
    if platform.system() == "Windows":
        mapa.save("C:\\index.html")
    else:
        mapa.save("/tmp/index.html")


if __name__ == "__main__":
    loop_last("", "")
