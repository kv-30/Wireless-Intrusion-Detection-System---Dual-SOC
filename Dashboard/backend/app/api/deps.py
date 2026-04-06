# deps.py
from fastapi import Depends, WebSocket
from app.core.ws_manager import connect, disconnect

async def ws_dependency(ws: WebSocket, layer: str):
    await connect(ws, layer)
    try:
        yield ws
    finally:
        await disconnect(ws, layer)