from mongoengine import Document, StringField, ReferenceField
from .user import User


class HiringManager(Document):
    user = ReferenceField(User)
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    current_jobrole = StringField()
    company_description = StringField()
    founded = StringField()  
    website = StringField()
    company_size = StringField()
    city = StringField()
    state = StringField()
    company_name = StringField(required=True)
