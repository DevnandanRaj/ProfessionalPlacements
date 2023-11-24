from mongoengine import Document, StringField, ReferenceField


class Application(Document):
    status = StringField(required=True)
    job_posting = ReferenceField('JobPosting')
    job_seeker = ReferenceField('JobSeeker')
