# coding: utf-8

from __future__ import unicode_literals

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from queue import NotificationRunner


class ListenForEvent(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self)
        self.config = config
        self.runner = NotificationRunner(self)

    def onConnect(self):
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        # callback = lambda x: log.msg("Received event %s" % x)
        # yield self.subscribe(callback, 'un_evenement')
        print("session ready")
        yield self.runner.connect()


# Start reactor here
if __name__ == '__main__':
    runner = ApplicationRunner("ws://localhost:8081/ws", "messaging")
    runner.run(ListenForEvent)
