# coding: utf-8

from pprint import pprint
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from phpserialize import loads

from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

import redis


class AuthenticatorSession(ApplicationSession):

    def __init__(self, config):
        ApplicationSession.__init__(self)
        self.config = config
        r_server = redis.StrictRedis(
                host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.redis = r_server

    @inlineCallbacks
    def onJoin(self, details):

        def load_token(token):
            key = self.redis.get("api:tokens:" + token)
            return key

        def authenticate(realm, authid, details):
            print("WAMP-Anonymous dynamic authenticator invoked: realm='{}', authid='{}'".format(realm, authid))
            ticket = details['ticket']
            # pprint(details)

            data = load_token(ticket)
            if data is None:
                raise ApplicationError(u"no_such_user", u"could not authenticate session - no such principal {}".format(authid))

            ticket = loads(data)
            # ticket holds 5 values!!!
            user_id, login, password, roles, is_enabled = ticket.values()

            if authid == login:
                principal = {
                    u'role': u'public',
                    u'extra': {
                        u'session': details['session']
                    }
                }
                return principal
            else:
                error = u"could not authenticate session - invalid ticket '{}' for principal {}".format(ticket, authid)
                raise ApplicationError(u"invalid_ticket", error)

        try:
            yield self.register(authenticate, 'authenticate')
            print("WAMP-Anonymous dynamic authenticator registered!")
        except Exception as e:
            print("Failed to register dynamic authenticator: {0}".format(e))