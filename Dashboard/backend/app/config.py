# backend/app/config.py
import os

# Core logic removed for IP protection.
# Sensitive defaults have been replaced with placeholders.

# ---------------- InfluxDB 2.x Settings ----------------
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "YOUR_INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "your-org")

# Use the bucket names exactly as you requested
BUCKET_BRONZE = os.getenv("BUCKET_BRONZE", "bronze_layer")
BUCKET_SILVER = os.getenv("BUCKET_SILVER", "silver_layer")
BUCKET_GOLD = os.getenv("BUCKET_GOLD", "gold_layer")

# ---------------- ML API Settings ----------------
ML_API_URL = os.getenv("ML_API_URL", "http://localhost:5001/predict")
ML_TIMEOUT = int(os.getenv("ML_TIMEOUT", "5"))

# ---------------- WebSocket Settings ----------------
WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
WS_PORT = int(os.getenv("WS_PORT", "8765"))
WS_MAX_CLIENTS = int(os.getenv("WS_MAX_CLIENTS", "50"))

# ---------------- MQTT Settings ----------------
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "network/packets")

# ---------------- Rolling Window Settings ----------------
WINDOW_SIZE = float(os.getenv("WINDOW_SIZE", "1.0"))    # seconds
ROLLING_SIZE = int(os.getenv("ROLLING_SIZE", "10"))     # number of windows

# ---------------- Detection Tuning ----------------
SILVER_LOOKBACK_SECONDS = int(os.getenv("SILVER_LOOKBACK_SECONDS", "90"))
GOLD_LOOKBACK_SECONDS = int(os.getenv("GOLD_LOOKBACK_SECONDS", "180"))
ML_ATTACK_THRESHOLD = float(os.getenv("ML_ATTACK_THRESHOLD", "0.4"))
GOLD_PROCESS_INTERVAL = float(os.getenv("GOLD_PROCESS_INTERVAL", "1.0"))