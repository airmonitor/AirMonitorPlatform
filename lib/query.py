# coding=utf-8

from configparser import ConfigParser
import os

from influxdb import InfluxDBClient

from lib.airmonitor_common_libs import logger_initialization

LOGGER = logger_initialization()
LOG_LEVEL = os.environ["LOG_LEVEL"]
CONFIGURATION_FILE_PATH = os.environ["CONFIGURATION_FILE_PATH"]

parser = ConfigParser()
parser.read(CONFIGURATION_FILE_PATH)

airmonitor_database_ec2_name = (parser.get('airmonitor', 'airmonitor_database_ec2_name'))
airmonitor_database_port = (parser.get('airmonitor', 'airmonitor_database_port'))
airmonitor_database_username = (parser.get('airmonitor', 'airmonitor_database_username'))
airmonitor_database_password = (parser.get('airmonitor', 'airmonitor_database_password'))
airmonitor_database = (parser.get('airmonitor', 'airmonitor_database'))

client = InfluxDBClient(
    host=airmonitor_database_ec2_name,
    port=airmonitor_database_port,
    username=airmonitor_database_username,
    password=airmonitor_database_password,
    database=airmonitor_database,
    ssl=True,
    verify_ssl=False,
    timeout=10
)


def query(sensor_value, lat, long):
    if lat != ("0" or "50"):
        influxdb_query = f"SELECT LAST(value) FROM {sensor_value} WHERE lat = '{lat}' " \
            f"AND long = '{long}' " \
            f"AND time > now() - 3h"

        LOGGER.debug("query: %s", influxdb_query)
        point_value = client.query(influxdb_query)
        LOGGER.debug("point_value: %s", point_value)
        return point_value
