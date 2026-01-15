from pika import BlockingConnection
from datetime import datetime, timezone
from app.core import settings
import requests

def writing_to_file(response):
    try:
        with open('./responses_tg.txt', 'a') as file:
            file.write(f"{datetime.now(tz=timezone.utc).strftime('%Y-%m-%d (%H:%M)')} - {response}\n")
    except Exception as e:
        print('Не удалось записать ответ в файл', e)

def processing_message(ch, method, properties, body: bytes):
    try:
        url = settings.telegram.get_telegram_url_send_msg
        params = {'chat_id': settings.telegram.TELEGRAM_BOT_CHAT_ID, 'text': {body.decode('utf-8')}}
        response = requests.post(url, params=params)
        abc = response.json()
        writing_to_file(response.json())
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    with BlockingConnection(parameters=settings.rabbitmq.get_rabbitmq_url) as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange='telegram_exchange', exchange_type='direct', durable=True)
            telegram_queue = channel.queue_declare(queue='telegram_queue', durable=True)
            channel.queue_bind(exchange='telegram_exchange', queue=telegram_queue.method.queue, routing_key='tg_key')
            channel.basic_consume(queue=telegram_queue.method.queue, auto_ack=False, on_message_callback=processing_message)
            channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        pass