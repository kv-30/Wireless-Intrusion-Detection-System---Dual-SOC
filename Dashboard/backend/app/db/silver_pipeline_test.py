# backend/app/db/silver_pipeline_test.py
import logging
from datetime import datetime, timedelta, timezone
import pandas as pd
from influxdb_client import InfluxDBClient, Point
from app.config import BUCKET_BRONZE, INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, WINDOW_SIZE
from app.processing.silver_pipeline import fetch_bronze, compute_silver_features, logger as silver_logger

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO, format='[Silver Test] %(levelname)s: %(message)s')
logger = logging.getLogger("Silver Test")

# ---------------- InfluxDB Client ----------------
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api()

# ---------------- Test Bronze Data Injection ----------------
def inject_test_bronze(num_points=10, subtype="wifi"):
    logger.info("Injecting test Bronze data...")
    for i in range(num_points):
        point = (
            Point("raw_packets")
            .tag("src", f"00:11:22:33:44:{i:02d}")
            .tag("dst", f"AA:BB:CC:DD:EE:{i:02d}")
            .tag("subtype", subtype)
            .field("rssi", -50 + i)  # integer RSSI to avoid type conflict
            .time(datetime.now(timezone.utc) - timedelta(seconds=i * 5))
        )
        write_api.write(bucket=BUCKET_BRONZE, record=point)
    logger.info(f"{num_points} test Bronze points injected.")

# ---------------- Test Silver Pipeline ----------------
def test_silver_pipeline():
    logger.info("Fetching Bronze data from Silver pipeline fetch_bronze...")
    df_bronze = fetch_bronze(subtype_val="wifi")
    
    if df_bronze.empty:
        logger.warning("No Bronze data fetched.")
        return
    
    logger.info(f"Fetched {len(df_bronze)} Bronze rows")
    logger.info(f"Columns: {df_bronze.columns.tolist()}")
    
    df_silver = compute_silver_features(df_bronze)
    if df_silver is None or df_silver.empty:
        logger.warning("Skipping Silver computation: no features computed")
    else:
        logger.info(f"Silver features computed: {len(df_silver)} rows")
        logger.info(f"Columns: {df_silver.columns.tolist()}")
        logger.debug(f"Sample data:\n{df_silver.head()}")

# ---------------- Main ----------------
if __name__ == "__main__":
    inject_test_bronze()
    test_silver_pipeline()
    logger.info("Silver pipeline test completed.")