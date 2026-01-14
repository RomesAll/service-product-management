from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from datetime import datetime, timezone

connection_parameters = ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=PlainCredentials(username='guest', password='guest')
)

def processing_message(ch, method, properties, body: bytes):
    pass

def main():
    with BlockingConnection(parameters=connection_parameters) as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange='telegram_exchange', exchange_type='direct', durable=True)
            telegram_queue = channel.queue_declare(queue='telegram_queue', durable=True)
            channel.queue_bind(exchange='telegram_exchange', queue=telegram_queue.method.queue, routing_key='tg_key')
            channel.basic_consume(queue=telegram_queue.method.queue, auto_ack=False, on_message_callback=processing_message)
            channel.start_consuming()

if __name__ == '__main__':
    main()