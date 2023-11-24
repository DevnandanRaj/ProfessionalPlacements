from mongoengine import Document, StringField, ReferenceField


class SkillSet(Document):
    skills = StringField(required=True)
    job_posting = ReferenceField('JobPosting')
