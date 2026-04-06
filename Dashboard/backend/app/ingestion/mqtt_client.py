# backend/app/ingestion/mqtt_client.py
import asyncio
import json
import logging
from app.db.bronze import write_bronze
import paho.mqtt.client as mqtt
from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

logger = logging.getLogger("MQTT Client")

def _normalize_payload(payload: dict) -> dict:
    """
    Normalize common ESP32/WiFi sniffer payload variants to Bronze schema.
    Expected Bronze keys: src, dst, subtype, rssi
    """
    src = payload.get("src") or payload.get("source") or payload.get("src_mac") or payload.get("sa")
    dst = payload.get("dst") or payload.get("destination") or payload.get("dst_mac") or payload.get("da")
    subtype = payload.get("subtype") or payload.get("frame_subtype") or payload.get("type") or "unknown"
    rssi = payload.get("rssi")
    if rssi is None:
        rssi = payload.get("signal")
    if rssi is None:
        rssi = payload.get("signal_dbm")

    return {
        "src": src or "unknown",
        "dst": dst or "unknown",
        "subtype": str(subtype),
        "rssi": float(rssi if rssi is not None else 0.0),
    }


# ---------------- MQTT CALLBACKS ----------------
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker successfully.")
        client.subscribe(MQTT_TOPIC)
        logger.info(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        logger.error(f"Failed to connect to MQTT broker, rc={rc}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Disconnected from MQTT broker unexpectedly (rc=%s). Reconnecting...", rc)
    else:
        logger.info("Disconnected from MQTT broker.")


def on_message(client, userdata, msg):
    """
    Callback for incoming MQTT messages.
    Write to InfluxDB Bronze layer and push to asyncio queue for WS broadcast.
    """
    try:
        payload = json.loads(msg.payload.decode())
        normalized = _normalize_payload(payload)

        # Write raw packets to Bronze layer
        write_bronze([normalized])
        logger.info(
            "[MQTT] Packet ingested: topic=%s src=%s dst=%s subtype=%s rssi=%s",
            msg.topic,
            normalized.get("src"),
            normalized.get("dst"),
            normalized.get("subtype"),
            normalized.get("rssi"),
        )

    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")


# ---------------- MQTT CLIENT START ----------------
async def start_mqtt():
    """
    Start MQTT client and continuously forward messages to WebSocket clients.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.reconnect_delay_set(min_delay=2, max_delay=30)

    # Connect with retry so backend stays alive even if broker is temporarily unreachable
    connected = False
    while not connected:
        try:
            logger.info(
                "Connecting to MQTT broker: broker=%s port=%s topic=%s",
                MQTT_BROKER,
                MQTT_PORT,
                MQTT_TOPIC,
            )
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_start()
            connected = True
            logger.info("MQTT client started and reconnect logic enabled.")
        except Exception as e:
            logger.error("MQTT connect failed (%s). Retrying in 5s...", e)
            await asyncio.sleep(5)

    # Keep coroutine alive for app lifecycle
    while True:
        await asyncio.sleep(1)