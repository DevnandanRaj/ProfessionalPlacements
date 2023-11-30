from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField
from .user import User
from datetime import datetime

class Degree(Document):
    type = StringField(required=True)
    college_name = StringField(required=True)
    course_name = StringField(required=True)
    marks = StringField(required=True)
    start_date = DateTimeField()
    end_date = DateTimeField()


class JobSeeker(Document):
    user = ReferenceField(User)
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    education = StringField()
    phone = StringField()
    address = StringField()
    city = StringField()
    state = StringField()
    pincode = StringField()
    status = StringField(required=True)
    skills = ListField(StringField(), required=True)
    experience = StringField(required=True)
    bio = StringField()
    degrees = ListField(ReferenceField(Degree))



