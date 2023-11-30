from mongoengine import Document, ListField, EmbeddedDocument, StringField, ReferenceField, DateField, EmbeddedDocumentField
from .job_posting import JobPosting
from .hiring_manager import HiringManager


class Job(EmbeddedDocument):
    job_title = StringField()
    status = StringField()
    start_date = DateField()
    end_date = DateField()
    hiring_manager = ReferenceField(HiringManager)
    job_description = StringField()
    salary = StringField()
    graduation = StringField()
    postgraduation = StringField()
    location = StringField()
    role_category = StringField()
    department = StringField()
    experience = StringField()
    required_skills = ListField(StringField())
    prefered_skills = ListField(StringField())
    employment_type = StringField()
    openings = StringField()
    timestamp = DateField()


class SkillSet(Document):
    skills = ListField(required=True)
    jobs = ListField(EmbeddedDocumentField(Job))
