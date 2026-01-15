from app.core import settings
from pika import BlockingConnection

def publish_telegram_bot_message(event, title: str, message):
    with BlockingConnection(parameters=settings.rabbitmq.get_rabbitmq_url) as conn:
        with conn.channel() as channel:
            channel.exchange_declare(exchange='telegram_exchange', exchange_type='direct', durable=True)
            telegram_queue = channel.queue_declare(queue='telegram_queue', durable=True)
            channel.queue_bind(exchange='telegram_exchange', queue=telegram_queue.method.queue, routing_key='tg_key')
            channel.basic_publish(exchange='telegram_exchange', routing_key='tg_key', body=f"(Event: {event}) Title: {title.upper()} Message: {message}")