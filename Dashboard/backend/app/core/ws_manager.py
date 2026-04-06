# backend/app/core/ws_manager.py
import asyncio
import logging
from fastapi import WebSocket
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"[WS Manager] Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"[WS Manager] Client disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"[WS Manager] Failed to send: {e}")

# Singleton instance
manager = ConnectionManager()

# Module-level helpers for easy import
connect = manager.connect
disconnect = manager.disconnect
broadcast = manager.broadcast

async def start():
    logger.info("[WS Manager] WebSocket manager started")

async def stop():
    logger.info("[WS Manager] WebSocket manager stopped")
    for ws in list(manager.active_connections):
        await ws.close()