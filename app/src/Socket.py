import os
from urllib.parse import urlparse
import redis
channel = 'test'

redis_url = os.getenv('REDIS_URL')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASS')

connection = redis.StrictRedis.from_url(
    url=redis_url, port=redis_port, db=0, password=redis_password, decode_responses=True)


class PubSubListener():
    def __init__(self):
        self.clients = []
        self.pubsub = connection.pubsub(ignore_subscribe_messages=False)
        self.pubsub.subscribe(**{channel: self.handler})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.001)

    def register(self, client):
        self.clients.append(client)

    def handler(self, message):
        _message = message['data']

        if type(_message) != int:
            self.send(_message)

    def send(self, data):
        for client in self.clients:
            try:
                client.send(data)
            except Exception:
                self.clients.remove(client)
