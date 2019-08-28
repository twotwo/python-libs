# -*- coding: utf-8 -*-
############################################################
#
# Consumer inside Thread
#
############################################################
import os
import time
import pika
from pika.exceptions import AMQPConnectionError
from loguru import logger
import multiprocessing
# add to make multiprocessing work (this way multiprocessing will not use fork).
multiprocessing.set_start_method('spawn', True)


def get_connection():
    logger.warning(f"connet to {os.getenv('RABBITMQ_HOST', 'dev.gpu')}")
    return pika.BlockingConnection(pika.ConnectionParameters(os.getenv(
        'RABBITMQ_HOST', 'dev.gpu'), credentials=pika.PlainCredentials('guest', os.getenv('RABBITMQ_PASS', 'guest'))))


def emit_log(channel, message):
    try:
        logger.debug("sending ...")
        # channel.basic_publish(exchange='', routing_key='hello', body=message)
        channel.basic_publish(
            exchange='logs', routing_key='logs.test', body=message)

        logger.info("[x] Sent '%s'" % message)
    except Exception as ex:
        raise ex


def receive_logs(connection):
    logger.debug("ENTERED")
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host='dev.gpu'))
    connection = get_connection()
    logger.debug("1")
    channel = connection.channel()
    logger.debug("2")
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    logger.debug("3")
    result = channel.queue_declare(exclusive=True)
    logger.debug("4")
    queue_name = result.method.queue
    logger.debug("5")

    def callback_rabbit(ch, method, properties, body):
        logger.debug(f"RICEVUTO MSG: RKEY: {method.routing_key}, {body}")

    logger.debug("6")
    channel.queue_bind(exchange='logs', queue=queue_name,
                       routing_key='#')
    logger.debug("7")
    # channel.basic_consume(callback_rabbit, queue=queue_name, no_ack=True)
    # logger.debug("8")
    # channel.start_consuming()
    try:
        for method, properties, body in channel.consume(queue=queue_name, no_ack=True):
            callback_rabbit(channel, method, properties, body)
    except AMQPConnectionError as er:
        logger.error(f'channel.consume failed, er: {er}')
    except KeyboardInterrupt:
        logger.info('exit ...')


def start():
    connection = get_connection()
    connection = None
    t_msg = multiprocessing.Process(target=receive_logs, args=(connection, ))
    t_msg.start()
    t_msg.join(0)


if __name__ == '__main__':
    start()
    time.sleep(1)

    connection = get_connection()
    channel = connection.channel()

    logger.debug("create exchange ...")
    channel.exchange_declare(exchange='logs', exchange_type='topic')
    logger.warning('begin send')
    for i in range(10):
        emit_log(channel, f'[{i}] hello')
