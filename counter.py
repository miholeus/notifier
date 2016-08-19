# coding: utf-8

from __future__ import unicode_literals

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

from config.settings import REALM_NAME, WEB_SOCKET_HOST, WEB_SOCKET_PORT


class ListenForEvent(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self)
        self.config = config

    def onConnect(self):
        print("connected")
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        # callback = lambda x: log.msg("Received event %s" % x)
        # yield self.subscribe(callback, 'un_evenement')
        print("session ready")

        counter = 0
        while True:
            self.publish('com.messaging.demo', counter)
            counter += 1
            yield sleep(1)

# Python doesn't have a default event loop, so
# we need to start one
if __name__ == '__main__':
    runner = ApplicationRunner("ws://%s:%d/ws" % (WEB_SOCKET_HOST, WEB_SOCKET_PORT), REALM_NAME)
    runner.run(ListenForEvent)
