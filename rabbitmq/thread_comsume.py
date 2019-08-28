# -*- coding: utf-8 -*-
############################################################
#
# Consumer inside Thread
#
############################################################
import os
import pika
from loguru import logger
import multiprocessing
# add to make multiprocessing work (this way multiprocessing will not use fork).
multiprocessing.set_start_method('spawn', True)


def emit_log(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'dev.gpu', credentials=pika.PlainCredentials('guest', os.getenv("RABBITMQ_PASS", 'guest'))))
        channel = connection.channel()

        logger.debug("create exchange ...")
        channel.exchange_declare(exchange='logs', exchange_type='topic')

        logger.debug("sending ...")
        # channel.basic_publish(exchange='', routing_key='hello', body=message)
        channel.basic_publish(exchange='logs', routing_key='', body=message)

        logger.info("[x] Sent '%s'" % message)
        connection.close()
    except Exception as ex:
        raise ex


def receive_logs():
    logger.debug("ENTERED")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='dev.gpu'))
    # connection = pika.BlockingConnection(pika.ConnectionParameters(
    #     'dev.gpu', credentials=pika.PlainCredentials('guest', os.getenv("RABBITMQ_PASS", 'guest'))))
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
                       routing_key='test.routing.key')
    logger.debug("7")
    channel.basic_consume(callback_rabbit, queue=queue_name, no_ack=True)
    logger.debug("8")
    channel.start_consuming()


def start():
    # t_msg = threading.Thread(target=receive_logs)
    t_msg = multiprocessing.Process(target=receive_logs, args=())
    t_msg.start()
    t_msg.join(0)


if __name__ == '__main__':
    # receive_logs()
    start()
    logger.warning('begin send')
    for i in range(10):
        emit_log(f'[{i}] hello')
