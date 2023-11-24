from mongoengine import Document, StringField, DateTimeField, ReferenceField
from .user import User

class JobSeeker(Document):
    user = ReferenceField(User)
    name = StringField(required=True)
    status = StringField(required=True)
    skills = StringField(required=True)
    experience = StringField(required=True)
    bio = StringField()
