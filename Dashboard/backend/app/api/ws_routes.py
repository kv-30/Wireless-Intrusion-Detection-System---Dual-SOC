from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.ws_manager import connect, disconnect

router = APIRouter()

@router.websocket("/ws/metrics")
async def websocket_metrics(ws: WebSocket):
    await connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        disconnect(ws)
    except Exception:
        disconnect(ws)


@router.websocket("/ws")
async def websocket_legacy(ws: WebSocket):
    """Backward-compatible alias for older frontend clients."""
    await connect(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        disconnect(ws)
    except Exception:
        disconnect(ws)