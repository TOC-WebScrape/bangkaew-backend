import os
import asyncio
import async_timeout
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from redis import asyncio as aioredis
from .notifier import Notifier
from fastapi.responses import HTMLResponse


redis_url = os.getenv('REDIS_URL')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASS')


app = FastAPI()
redis = aioredis.from_url(
    f"{redis_url}:{redis_port}", password=redis_password, decode_responses=True)
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
    <ul id='messages'>
    <script type="text/javascript">
      const ws = new WebSocket("ws://localhost:5000/ws");
      ws.send({"request": ["BTC", "ETH"]})
      const messages = document.getElementById('messages')
      ws.onmessage = function (event) {
        console.log(event.data);
        const message = document.createElement('li')
        const content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
      };
    </script>
  </body>
</html>
"""


PUBSUB = None


async def init_pubsub():
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await PUBSUB.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    print(f"(Reader) Message Received: {message}")
                    data = message["data"]
                    room = message["channel"][len("channel:"):]
                    await notifier._notify({"data": data, "room": room}, room)
                    if message["data"] == STOPWORD:
                        print("(Reader) STOP")
                        break
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


async def consumer_handler(ws: WebSocket):
    try:
        while True:
            message = await ws.receive_json()
            if (len(message["request"]) > 0):
                await notifier.request_room(ws, message["request"])

    except WebSocketDisconnect as exc:
        pass


@app.on_event('startup')
async def startup_event():
    global PUBSUB
    pubsub = redis.pubsub()
    await pubsub.psubscribe("channel:*")
    PUBSUB = pubsub
    asyncio.create_task(init_pubsub())


@app.get("/")
async def get():
    return HTMLResponse(html)

STOPWORD = "END"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # rooms_req = websocket.query_params["room_name"]
    # room_names = rooms_req.split(',')
    # room_names = [room_name]
    await notifier.connect(websocket)
    done, pending = await asyncio.wait(
        [consumer_handler], return_when=asyncio.FIRST_COMPLETED,
    )
    print(f"Done task: {done}")
    for task in pending:
        task.cancel()
