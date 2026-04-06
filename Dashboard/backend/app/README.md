# -------------------- backend/app/README.md --------------------
# Backend Service - Wireless IDS

This folder contains the backend service of the Wireless IDS project.  
It is responsible for:

1. Ingesting Wi-Fi probe request frames from ESP32 devices (blue and red team sensors) via MQTT.
2. Storing raw data in InfluxDB (Bronze layer) and processing it into Silver and Gold layers.
3. Running real-time pipelines for feature extraction, aggregation, and attack detection.
4. Calling the ML microservice (Random Forest API) for predictions.
5. Streaming live data to the frontend via WebSockets.

## Folder Structure

backend/app/
├── main.py                 # FastAPI entrypoint
├── config.py               # Configs (MQTT, DB, ML API)
├── api/                    # REST API endpoints for frontend
│   ├── routes.py           # InfluxDB queries
│   └── deps.py             # Dependency injection helpers
├── core/                   # Core infrastructure utilities
│   ├── ws_manager.py       # WebSocket manager
│   ├── queue.py            # In-memory queue for buffering frames
│   └── backpressure.py     # Prevent system overload
├── ingestion/              # Data ingestion
│   └── mqtt_client.py      # MQTT subscriber
├── processing/             # Data pipelines
│   ├── pipeline.py         # Calls ML API
│   ├── buffer.py           # In-memory buffering
│   ├── feature_extractor.py
│   ├── aggregator.py       # Aggregate features into Silver/Gold layers
│   └── fallback_detector.py
├── ml_client/              # ML API integration
│   ├── rf_client.py
│   └── retry.py
├── db/                     # InfluxDB clients
│   ├── influx_client.py
│   ├── bronze.py
│   ├── silver.py
│   └── gold.py
└── utils/
    ├── logger.py
    ├── metrics.py
    └── time.py

## Running Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload