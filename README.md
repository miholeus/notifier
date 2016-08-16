Realtime messaging support for ISUP project

Messaging is based on websockets.
Publisher takes messages from RabbitMQ and sends them to consumers.
Consumers are connected through queue bindings.