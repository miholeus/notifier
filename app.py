# coding: utf-8

from __future__ import unicode_literals

from twisted.python import log
from twisted.internet.defer import inlineCallbacks

# autobahn is the de facto Python lib to build
# WAMP clients
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner


class ListenForEvent(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self)
        self.config = config

    def onConnect(self):
        self.join(self.config.realm)

    @inlineCallbacks
    def onJoin(self, details):
        callback = lambda x: log.msg("Received event %s" % x)
        yield self.subscribe(callback, 'un_evenement')

# Python doesn't have a default event loop, so
# we need to start one
if __name__ == '__main__':
    runner = ApplicationRunner("ws://localhost:8081/ws", "messaging")
    runner.run(ListenForEvent)
