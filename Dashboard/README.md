
---

```markdown
# wireless-ids/README.md

# Wireless IDS - Full Repo Overview

This repository implements a **Wireless Intrusion Detection System (IDS)** using ESP32 devices, real-time data processing, ML-based detection, and a dashboard.

## Repo Structure

wireless-ids/
├── backend/            # Backend FastAPI service
├── ml-service/         # ML Flask microservice (Random Forest API)
├── frontend/           # ReactJS dashboard
├── ml-training/        # Training scripts and feature config
├── docker/             # Dockerfiles + docker-compose
├── .env
└── README.md

## Workflow

1. ESP32 (blue team) sends probe requests via MQTT.
2. Backend ingests raw frames into Bronze layer.
3. Silver layer: features extracted and aggregated.
4. Gold layer: enriched data with ML predictions (Random Forest API).
5. Frontend dashboard consumes Silver/Gold layers for real-time visualization.
6. Parallel ML processing ensures predictions and dashboard updates run simultaneously.
7. Red team ESP32 can simulate attacks for testing and demonstration.

## How to Run

- Use `docker-compose up` to start all services:
  - Backend (FastAPI)
  - ML microservice (Flask)
  - Frontend (ReactJS)
- Ensure `.env` variables are set for DB, MQTT, and ML endpoints.

## Notes

- Supports **real-time streaming** and **historical data queries**.
- Bronze/Silver/Gold layers implement the **data analytics pipeline**.
- ML predictions run in parallel to Gold layer updates for efficiency.