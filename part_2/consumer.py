import pika
from mongoengine import connect
import time
from models import Contact



connect(host='mongodb+srv://katepomazunova:Dk12345678@cluster0.6ez0nqr.mongodb.net/HW8')

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    print(f"Sending email to {contact.name} ({contact.email})...")
    time.sleep(3)
    contact.message_sent = True
    contact.save()
    print(f"Email sent to {contact.name} ({contact.email}).")


def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {message}")
    send_email(message)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=True)


if __name__ == '__main__':
    channel.start_consuming()