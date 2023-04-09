from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    name = StringField()
    email = StringField()
    send_notification = BooleanField(default=False)