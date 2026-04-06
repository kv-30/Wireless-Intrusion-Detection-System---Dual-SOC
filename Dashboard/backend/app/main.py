# backend/app/main.py
import threading
import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.api.ws_routes import router as ws_router
from app.core import ws_manager
from app.ingestion import mqtt_client
from app.processing.silver_pipeline import run_silver
from app.processing.gold_pipeline import run_gold

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Wireless IDS Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(ws_router)

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    # WS Manager
    await ws_manager.start()

    # MQTT ingestion
    threading.Thread(
        target=lambda: asyncio.run(mqtt_client.start_mqtt()),
        daemon=True
    ).start()
    logger.info("MQTT ingestion started.")

    # Silver pipeline (threaded)
    threading.Thread(
    target=lambda: asyncio.run(run_silver()),
    daemon=True
    ).start()   

    # Gold pipeline (async)
    asyncio.create_task(run_gold())
    logger.info("Gold pipeline started.")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean shutdown"""
    await ws_manager.stop()
    logger.info("Shutdown complete.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)