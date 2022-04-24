import os
import logging
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import aioredis
from aioredis.client import PubSub, Redis
from .notifier import Notifier
from fastapi.responses import HTMLResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


redis_url = os.getenv('REDIS_URL')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASS')


app = FastAPI()
notifier = Notifier()

html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Test Websocket</title>
  </head>
  <body>
    <h1>Request Subscript</h1>
    <form action="" onsubmit="reqMessage(event)">
        <input type="text" id="reqText" autocomplete="off"/>
        <button>Send</button>
    </form>
    <h1>Revoke Subscript</h1>
    <form action="" onsubmit="revokeMessage(event)">
        <input type="text" id="revokeTaxt" autocomplete="off"/>
        <button>Send</button>
    </form>
    <ul id='messages'>
    <script type="text/javascript">
      const ws = new WebSocket("ws://localhost:5000/ws");
      const messages = document.getElementById('messages')
      ws.addEventListener('open', function (event){
        ws.send(JSON.stringify({"request": ["BTC", "ETH"]}));
      });
      ws.addEventListener('message', function (event){
        console.log(event.data);
        const message = document.createElement('li')
        const content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
      });
      function reqMessage(event) {
                var input = document.getElementById("reqText")
                ws.send(JSON.stringify({"request": [input.value]}))
                input.value = ''
                event.preventDefault()
        }
        function revokeMessage(event) {
                var input = document.getElementById("revokeTaxt")
                ws.send(JSON.stringify({"revoke": [input.value]}))
                input.value = ''
                event.preventDefault()
        }
    </script>
  </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

STOPWORD = "END"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    await redis_connector(websocket)


async def redis_connector(websocket: WebSocket):
    async def consumer_handler(ws: WebSocket):
        try:
            while True:
                message = await ws.receive_json()
                print(message)
                if "request" in message:
                    await notifier.request_room(websocket, message["request"])
                if "revoke" in message:
                    await notifier.revoke(ws, message["revoke"])
        except WebSocketDisconnect as exc:
            # TODO this needs handling better
            logger.error(exc)

    async def producer_handler(pubsub: PubSub):
        await pubsub.psubscribe("channel:*")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    print(f"(Reader) Message Received: {message}")
                    data = message["data"]
                    room = message["channel"][len("channel:"):]
                    await notifier._notify({"data": data, "room": room}, room)
                    if message["data"] == STOPWORD:
                        print("(Reader) STOP")
                        break
        except Exception as exc:
            # TODO this needs handling better
            logger.error(exc)

    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    consumer_task = consumer_handler(ws=websocket)
    producer_task = producer_handler(pubsub=pubsub)
    done, pending = await asyncio.wait(
        [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
    )
    logger.debug(f"Done task: {done}")
    for task in pending:
        logger.debug(f"Canceling task: {task}")
        task.cancel()


async def get_redis_pool():
    return await aioredis.from_url(f"{redis_url}:{redis_port}", password=redis_password, encoding="utf-8", decode_responses=True)
