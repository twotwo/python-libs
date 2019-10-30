# -*- coding: utf-8 -*-
import typing

import pika
import pika.exceptions


class RabbitMQ(object):

    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None
        self.is_open = False

    def open(self):
        '''
        don't open connection until inside thread!
        '''
        if self.is_open:
            return
        self.connection = pika.BlockingConnection(
            pika.URLParameters(self.amqp_url))
        self.channel = self.connection.channel()
        self.is_open = True

    def bind(self, exchange: str, routing_key: str, queue: str, durable: bool = True):
        self.channel.exchange_declare(
            exchange=exchange, exchange_type='topic', durable=durable)
        self.channel.queue_declare(queue=queue, durable=durable)
        self.channel.queue_bind(queue, exchange, routing_key=routing_key)

    def cancel(self):
        self.channel.cancel()

    def close(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except pika.exceptions.AMQPError:
            pass
        finally:
            self.is_open = False

    def __repr__(self):
        return self.amqp_url


class MQProducer(RabbitMQ):

    def publish(self, exchange: str, routing_key: str, body: str,
                properties: pika.BasicProperties = None, mandatory: bool = True):
        if properties is None:
            properties = pika.BasicProperties(content_type='application/json')
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=body,
                                   properties=properties,
                                   mandatory=mandatory)


class MQConsumer(RabbitMQ):

    def open(self, prefetch: int = 200):
        """
        :param prefetch: prefetch count of message
        """
        super(MQConsumer, self).open()
        self.channel.basic_qos(prefetch_count=prefetch)

    def consume(self, queue: str):
        for method_frame, properties, body in self.channel.consume(queue):
            return method_frame, properties, body.decode('utf-8')

    def basic_consume(self, queue: str, on_message_callback: typing.Callable):
        self.channel.basic_consume(queue, on_message_callback)

    def start_consuming(self):
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

    def ack(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)
