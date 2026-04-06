# app/db/bronze.py
import logging
from influxdb_client import Point
from app.db.influx_client import write_api
from app.config import BUCKET_BRONZE

logger = logging.getLogger(__name__)

def write_bronze(frames: list):
    """
    Write raw frames to InfluxDB bronze bucket.

    - src and dst are stored as tags (categorical identifiers)
    - subtype and rssi are stored as fields (pivotable)
    """
    points = []

    try:
        for frame in frames:
            point = (
                Point("raw_packets")
                .tag("src", frame.get("src", "unknown"))
                .tag("dst", frame.get("dst", "unknown"))
                .field("subtype", frame.get("subtype", "unknown"))
                .field("rssi", float(frame.get("rssi", 0.0)))
            )
            points.append(point)

        if points:
            write_api.write(bucket=BUCKET_BRONZE, record=points)
            logger.info(f"Inserted {len(points)} raw frames into bronze bucket.")

    except Exception as e:
        logger.error(f"[Bronze DB] Error writing raw frames: {e}")