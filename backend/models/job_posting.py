from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField
from .hiring_manager import HiringManager

class JobPosting(Document):
    job_title = StringField(required=True)
    status = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    hiring_manager = ReferenceField(HiringManager)
    applications = ListField(ReferenceField('Application'))
    skill_sets = ListField(ReferenceField('SkillSet'))
    job_description = StringField(required=True)
