import pika
from mongoengine import connect
from datetime import datetime
import json
from faker import Faker
from models import Contact



NUM_CONTACTS = 10

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()
channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

connect(host='mongodb+srv://katepomazunova:Dk12345678@cluster0.6ez0nqr.mongodb.net/HW8')


def generate_contacts(num_contacts):
    fake = Faker()
    for i in range(num_contacts):
        name = fake.name()
        email = fake.email()
        Contact(name=name, email=email).save()


generate_contacts(NUM_CONTACTS)

for contact in Contact.objects:
    message = {
        'id': str(contact.id),
        'date': datetime.now().isoformat()
    }
    channel.basic_publish(
        exchange='task_mock', 
        routing_key="task_queue", 
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
    )

print(" [x] Sent %r" % message)

connection.close()
