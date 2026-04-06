# app/db/silver.py
import logging
import pandas as pd
from influxdb_client import Point
from app.db.influx_client import write_api
from app.config import BUCKET_SILVER

logger = logging.getLogger(__name__)


def _is_deauth_subtype(value) -> bool:
    """Return True when subtype value corresponds to a deauth frame."""
    if value is None:
        return False

    raw = str(value).strip().lower()

    # Common textual variants
    if raw in {"deauth", "deauthentication", "deauth_req", "deauth_request"}:
        return True

    # Hex-like forms seen from sniffers
    if raw in {"0x0c", "0xc"}:
        return True

    # Numeric forms (IEEE 802.11 deauth subtype is 12)
    try:
        if int(float(raw)) == 12:
            return True
    except (TypeError, ValueError):
        pass

    return False

# ---------------- Write Silver Features ----------------
def write_silver(features: dict):
    """
    Write extracted silver features to InfluxDB Silver bucket.
    src and dst are tags in Bronze, features are fields.
    """
    try:
        point = (
            Point("features")
            .field("num_deauth", float(features.get("num_deauth", 0)))
            .field("deauth_rate", float(features.get("deauth_rate", 0.0)))
            .field("unique_src_macs", float(features.get("unique_src_macs", 0)))
            .field("unique_dst_macs", float(features.get("unique_dst_macs", 0)))
            .field("mean_rssi", float(features.get("mean_rssi", 0.0)))
            .field("rssi_std", float(features.get("rssi_std", 0.0)))
            .field("inter_arrival_mean", float(features.get("inter_arrival_mean", 0.0)))
            .field("inter_arrival_std", float(features.get("inter_arrival_std", 0.0)))
            .field("max_burst_size", float(features.get("max_burst_size", 0)))
            .field("num_victims", float(features.get("num_victims", 0)))
            .field("victim_diversity", float(features.get("victim_diversity", 0.0)))
            .field("attacker_activity_level", float(features.get("attacker_activity_level", 0.0)))
        )
        write_api.write(bucket=BUCKET_SILVER, record=point)
        logger.info(f"Inserted Silver features into bucket '{BUCKET_SILVER}'.")
    except Exception as e:
        logger.error(f"[Silver DB] Error writing features: {e}")

# ---------------- Compute Features ----------------
def compute_features(df: pd.DataFrame):
    """
    Compute Silver features from Bronze dataframe.
    Assumes src and dst are tags; numeric fields like rssi exist in df.
    """
    if df is None or df.empty:
        return None

    # Ensure _time column is datetime
    df['_time'] = pd.to_datetime(df['_time'])

    features = {}

    # Basic counts
    subtype_series = df["subtype"] if "subtype" in df.columns else pd.Series([], dtype="object")
    deauth_mask = subtype_series.apply(_is_deauth_subtype)
    features["num_deauth"] = int(deauth_mask.sum())
    features["deauth_rate"] = features["num_deauth"] / max(len(df), 1)
    features["unique_src_macs"] = df["src"].nunique()
    features["unique_dst_macs"] = df["dst"].nunique()

    # RSSI stats
    features["mean_rssi"] = df["rssi"].mean() if "rssi" in df else 0
    features["rssi_std"] = df["rssi"].std() if "rssi" in df else 0

    # Inter-arrival stats
    inter = df['_time'].diff().dt.total_seconds().dropna()
    features["inter_arrival_mean"] = inter.mean() if not inter.empty else 0
    features["inter_arrival_std"] = inter.std() if not inter.empty else 0

    # Burst size & victims
    features["max_burst_size"] = df.groupby("src").size().max() if not df.empty else 0
    features["num_victims"] = df["dst"].nunique()
    features["victim_diversity"] = features["num_victims"] / max(len(df), 1)
    features["attacker_activity_level"] = features["unique_src_macs"] / max(len(df), 1)

    return features