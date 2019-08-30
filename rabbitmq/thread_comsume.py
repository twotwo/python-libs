# -*- coding: utf-8 -*-
############################################################
#
# Consumer inside Thread
#
############################################################
from rabbitmq import MQProducer, MQConsumer
import os
import time
import pika
from pika.exceptions import AMQPConnectionError
from loguru import logger
import multiprocessing
# add to make multiprocessing work (this way multiprocessing will not use fork).
multiprocessing.set_start_method('spawn', True)


def emit_log(mq_producer: MQProducer, message: str):
    try:
        logger.debug("sending ...")
        mq_producer.publish(
            exchange='logs', routing_key='logs.test', body=message)

        logger.info("[x] Sent '%s'" % message)
    except Exception as ex:
        raise ex


class SubClass(object):
    def __init__(self, conf: dict):
        self.amqp_url = conf.get('AMQP_URL')
        self.exchange = conf.get('EXCHANGE')
        self.routing_key = conf.get('ROUTING_KEY')
        self.mq_consumer = MQConsumer(self.amqp_url)
        # self.mq_consumer.open()

    def run(self):
        self.mq_consumer.open()
        queue_name = f"test-{self.exchange}"
        self.mq_consumer.bind(self.exchange, self.routing_key, queue_name)
        self.mq_consumer.basic_consume(queue_name, self.callback_rabbit)
        logger.warning(
            f"binding from {self.exchange}, routing_key={self.routing_key}, queue={queue_name}")
        self.mq_consumer.start_consuming()

    @classmethod
    def callback_rabbit(cls, ch, method, properties, body):
        logger.debug(f"RICEVUTO MSG: RKEY: {method.routing_key}, {body}")


def start():
    """
    a demo for use mq comsume in thread, give all params to subclass
    """
    conf = {
        'AMQP_URL': os.getenv('AMQP_URL', 'amqp://guest:guest@dev.gpu:5672'),
        'EXCHANGE': 'test',
        'ROUTING_KEY': '#'
    }
    subclass = SubClass(conf)
    process = multiprocessing.Process(target=subclass.run, args=())
    process.start()
    process.join(0)


if __name__ == '__main__':
    start()

    mq_producer = MQProducer(
        os.getenv('AMQP_URL', 'amqp://guest:guest@dev.gpu:5672'))
    mq_producer.open()
    logger.warning('begin send')
    for i in range(10):
        emit_log(mq_producer, f'[{i}] hello')

    mq_producer.close()
