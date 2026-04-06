# backend/app/db/pipeline_e2e_test.py
import logging
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
import pandas as pd

from app.config import BUCKET_BRONZE, INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG
from app.processing.silver_pipeline import fetch_bronze, compute_silver_features, write_silver
from app.processing.gold_pipeline import fetch_silver, compute_metrics, write_gold

logging.basicConfig(level=logging.INFO, format='[Pipeline E2E Test] %(levelname)s: %(message)s')
logger = logging.getLogger("Pipeline E2E Test")

# ---------------- Influx Client ----------------
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api()

# ---------------- Step 1: Inject Bronze Data ----------------
def inject_test_bronze(n_points: int = 10):
    logger.info(f"Injecting {n_points} test Bronze points...")
    points = []
    for i in range(n_points):
        p = Point("raw_packets") \
            .tag("subtype", "wifi") \
            .tag("src", f"00:11:22:33:44:{i:02d}") \
            .tag("dst", "ff:ff:ff:ff:ff:ff") \
            .field("rssi", -50 + i) \
            .time(datetime.utcnow() - timedelta(seconds=i * 5))
        points.append(p)
    write_api.write(bucket=BUCKET_BRONZE, record=points)
    logger.info("Test Bronze points injected successfully.")

# ---------------- Step 2: Run Silver Pipeline ----------------
def run_silver_test():
    logger.info("Fetching Bronze data for Silver computation...")
    df = fetch_bronze(subtype_val="wifi")

    if df.empty:
        logger.warning("No Bronze data fetched for Silver.")
        return None

    logger.info(f"Fetched {len(df)} Bronze rows.")
    features = compute_silver_features(df)

    if features is not None and not features.empty:
        write_silver(features)
        logger.info(f"Silver features computed and written: {len(features)} rows.")
    else:
        logger.warning("No Silver features computed.")
        features = None

    return features

# ---------------- Step 3: Run Gold Pipeline ----------------
def run_gold_test():
    logger.info("Fetching Silver data for Gold computation...")
    df = fetch_silver()
    if df.empty:
        logger.warning("No Silver data fetched for Gold.")
        return

    metrics = compute_metrics(df)
    logger.info(f"Computed Gold metrics: {metrics}")
    write_gold(metrics)
    logger.info("Gold metrics written successfully.")

# ---------------- Main Test ----------------
if __name__ == "__main__":
    inject_test_bronze()
    run_silver_test()
    run_gold_test()
    logger.info("End-to-end pipeline test completed successfully.")