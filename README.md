Realtime messaging support 

### Notifier

Messaging is based on websockets.
Publisher takes messages from RabbitMQ and sends them to consumers.
Consumers are connected through queue bindings.

### Configuration

Create `config/local.py` file and set your own settings.

RabbitMQ settings
```
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
```

Redis settings
```
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_DB = '2'
```

WebSocket host and port for messaging
```
WEB_SOCKET_HOST = u'127.0.0.1'
WEB_SOCKET_PORT = 8081
```
