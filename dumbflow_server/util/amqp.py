import json
import logging
from time import sleep

from pika import BasicProperties, BlockingConnection, URLParameters
from pika.channel import Channel

logger = logging.getLogger(__name__)


class Codec:

    content_type = ''

    def encode(self, data):
        raise NotImplementedError()

    def decode(self, data):
        raise NotImplementedError()


class PlainCodec(Codec):
    content_type = 'text/plain'

    def encode(self, data):
        return data

    def decode(self, data):
        return data


class JSONCodec(Codec):

    content_type = 'application/json'

    def encode(self, data):
        return json.dumps(data)

    def decode(self, data):
        return json.loads(data)


class AMQPClient:
    def __init__(self, url, codec=JSONCodec()):
        self.parameters = URLParameters(url)
        self.codec = codec

    def _make_connection(self):
        return BlockingConnection(self.parameters)

    def publish(self, exchange: str, queue: str, msg: str):
        conn = self._make_connection()
        channel = conn.channel()

        try:
            properties = BasicProperties(content_type=self.codec.content_type,
                                         delivery_mode=2)

            channel.exchange_declare(exchange)
            channel.queue_declare(queue)
            channel.queue_bind(queue, exchange, queue)
            channel.basic_publish(
                exchange=exchange,
                routing_key=queue,
                body=self.codec.encode(msg),
                properties=properties,
            )

        finally:
            conn.close()

    def queue_bind(self, queue, exchange):

        conn = self._make_connection()
        channel = conn.channel()

        try:
            channel.exchange_declare(exchange)
            channel.queue_declare(queue)
            channel.queue_bind(queue, exchange, queue)
        finally:
            conn.close()
