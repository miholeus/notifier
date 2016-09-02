# coding: utf-8

# RabbitMQ settings
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
# Queue settings
NOTIFICATION_EXCHANGE = u'notification.exchange'
NOTIFICATION_QUEUE = u'notification.awaiting'
NOTIFICATION_ROUTING_KEY = u'send.notification'
# Web sockets settings
REALM_NAME = u'messaging'
WEB_SOCKET_HOST = u'127.0.0.1'
WEB_SOCKET_PORT = 8081

# redis conf
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '2'


try:
    from .local import *
except ImportError:
    pass
