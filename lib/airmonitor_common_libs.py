# coding=utf-8

import json
import logging
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = os.environ["API_URL"]
LOG_LEVEL = os.environ["LOG_LEVEL"]
GOOGLE_SPREADSHEET_NAME = os.environ["GOOGLE_SPREADSHEET_NAME"]
KEY_FILE_PATH = os.environ["KEY_FILE_PATH"]


def logger_initialization():
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(f'%(name)s %(asctime)s %(levelname)s %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    logger.setLevel(logging.DEBUG if LOG_LEVEL == "DEBUG" else logging.WARNING)
    return logger


# Google Docs
def get_spreadsheet_data():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_PATH, scope)
    file = gspread.authorize(credentials)  # authenticate with Google
    sheet = file.open(GOOGLE_SPREADSHEET_NAME).sheet1
    list_from_google_docs = sheet.get_all_values()
    return list_from_google_docs


def _data_from_google_docs():
    logger = logger_initialization()
    list_from_google_docs = get_spreadsheet_data()

    lat_from_google_spread = []
    long_from_google_spread = []
    pm_sensor_model_from_google_spread = []

    logger.debug("List from Google Docs %s", list_from_google_docs[0])

    for values in list_from_google_docs[1:]:
        long = values[3]
        lat = values[2]
        sensor_model = values[4].upper()

        lat_from_google_spread.append(lat)
        long_from_google_spread.append(long)
        pm_sensor_model_from_google_spread.append(sensor_model)

        logger.debug("Lat %s, Long %s, Sensor model %s", lat, long, sensor_model)

    return list(zip(lat_from_google_spread, long_from_google_spread, pm_sensor_model_from_google_spread))


def _send_data_to_api(data):
    url = API_URL
    resp = requests.post(url, timeout=10, data=json.dumps(data), headers={"Content-Type": "application/json"})

    return resp.status_code
