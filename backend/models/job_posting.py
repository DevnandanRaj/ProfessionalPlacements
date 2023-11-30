
from mongoengine import Document, StringField, DateField, ReferenceField, ListField
from .hiring_manager import HiringManager
from .application import Application
from datetime import datetime
class JobPosting(Document):
    job_title = StringField(required=True)
    status = StringField(required=True)
    start_date = DateField(required=True)
    end_date = DateField(required=True)
    hiring_manager = ReferenceField(HiringManager)
    applications = ListField(ReferenceField(Application))
    skill_sets = ListField(ReferenceField('SkillSet'))
    job_description = StringField(required=True)
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
    timestamp = DateField(default=datetime.utcnow)


