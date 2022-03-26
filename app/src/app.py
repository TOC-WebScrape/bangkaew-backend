from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from .Socket import PubSubListener

App = FastAPI()

pslistener = PubSubListener()


@App.get("/")
async def get():
    return "HI!!!"


@App.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):

    await ws.accept()

    pslistener.register(ws)
