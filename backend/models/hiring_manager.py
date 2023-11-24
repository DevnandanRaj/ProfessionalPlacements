from mongoengine import Document, StringField, ReferenceField
from .user import User

class HiringManager(Document):
    user = ReferenceField(User)
    name = StringField(required=True)
    company_name = StringField(required=True)
    # Other HiringManager fields
