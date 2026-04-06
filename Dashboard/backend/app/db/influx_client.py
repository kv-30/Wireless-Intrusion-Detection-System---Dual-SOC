# backend/app/db/influx_client.py
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from app.config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG

# Core logic removed for IP protection.
# InfluxDB client setup remains environment-driven.

influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = influx_client.write_api(write_options=SYNCHRONOUS)
query_api = influx_client.query_api()
