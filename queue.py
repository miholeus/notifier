# coding: utf-8

from __future__ import unicode_literals

from pika.adapters import twisted_connection
from twisted.internet import defer, reactor, protocol, task
from config.settings import *
from twisted.logger import Logger

import pika


class NotificationRunner:
    log = Logger()
    """
    Runs Notification consumer that publishes messages to user's channel
    """
    def __init__(self, wamp_session=None):
        credentials = pika.PlainCredentials(username=RABBITMQ_USER, password=RABBITMQ_PASS)
        self.parameters = pika.ConnectionParameters(credentials=credentials)
        self.client = protocol.ClientCreator(reactor, twisted_connection.TwistedProtocolConnection, self.parameters)
        self.session = wamp_session

    @defer.inlineCallbacks
    def start(self, connection):

        channel = yield connection.channel()

        exchange = yield channel.exchange_declare(exchange=NOTIFICATION_EXCHANGE, type='topic', durable=True)

        queue = yield channel.queue_declare(queue=NOTIFICATION_QUEUE, auto_delete=False, exclusive=False, durable=True)

        yield channel.queue_bind(
                exchange=NOTIFICATION_EXCHANGE, queue=NOTIFICATION_QUEUE, routing_key=NOTIFICATION_ROUTING_KEY
        )

        # yield channel.basic_qos(prefetch_count=1)

        queue_object, consumer_tag = yield channel.basic_consume(queue=NOTIFICATION_QUEUE, no_ack=False)

        l = task.LoopingCall(self.read, queue_object)

        l.start(0.01)

    @defer.inlineCallbacks
    def read(self, queue_object):

        ch, method, properties, body = yield queue_object.get()

        if body:
            self.log.info(body)
            if self.session:
                self.session.publish("notifications.user", body)

        yield ch.basic_ack(delivery_tag=method.delivery_tag)

    def connect(self):
        d = self.client.connectTCP(RABBITMQ_HOST, RABBITMQ_PORT)
        d.addCallback(lambda protocol: protocol.ready)
        d.addCallback(self.start)

    def run(self):
        """"
        Runs reactor
        """
        self.connect()
        reactor.run()

if __name__ == "__main__":
    runner = NotificationRunner()
    runner.run()
