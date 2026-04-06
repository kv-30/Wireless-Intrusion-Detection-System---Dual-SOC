# app/db/gold.py
import logging
from influxdb_client import Point
from app.db.influx_client import write_api
from app.config import BUCKET_GOLD

logger = logging.getLogger(__name__)

def write_gold(metrics: dict):
    """
    Write gold metrics (Silver features + ML predictions) to InfluxDB Gold bucket.
    
    Metrics include:
    - traffic: packet count
    - baseline: avg RSSI
    - avg_rssi: average signal strength
    - entropy: victim diversity
    - state: NORMAL or ATTACK
    - ml_confidence: probability of attack (0-1)
    - attack_detected: boolean flag
    """
    try:
        point = Point("aggregates") \
            .field("traffic", int(metrics.get("traffic", 0))) \
            .field("baseline", float(metrics.get("baseline", 0.0))) \
            .field("avg_rssi", float(metrics.get("avg_rssi", 0.0))) \
            .field("entropy", float(metrics.get("entropy", 0.0))) \
            .field("state", str(metrics.get("state", "NORMAL"))) \
            .field("attack_type", str(metrics.get("attack_type", "NONE"))) \
            .field("ml_confidence", float(metrics.get("ml_confidence", 0.0))) \
            .field("attack_detected", bool(metrics.get("attack_detected", False))) \
            .field("ml_prediction_code", int(metrics.get("ml_prediction_code", 0))) \
            .field("ml_prediction_label", str(metrics.get("ml_prediction_label", "normal")))

        # Optional tags for dashboard filtering
        if "top_attacker" in metrics:
            point = point.tag("top_attacker", str(metrics["top_attacker"]))
        if "top_victim" in metrics:
            point = point.tag("top_victim", str(metrics["top_victim"]))

        write_api.write(bucket=BUCKET_GOLD, record=point)
        logger.info(f"Written gold metrics to '{BUCKET_GOLD}': state={metrics.get('state')}")

    except Exception as e:
        logger.error(f"[Gold DB] Error writing metrics: {e}", exc_info=True)