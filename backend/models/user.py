from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField


class User(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True)  # 'hiring_manager' or 'job_seeker'
    created_at = DateTimeField()


class JobSeeker(Document):
    user = ReferenceField(User)
    name = StringField(required=True)
    status = StringField(required=True)
    skills = StringField(required=True)
    experience = StringField(required=True)
    bio = StringField()



class HiringManager(Document):
    user = ReferenceField(User)
    name = StringField(required=True)
    company_name = StringField(required=True)
    # Other HiringManager fields


class JobPosting(Document):
    job_title = StringField(required=True)
    status = StringField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    hiring_manager = ReferenceField(HiringManager)
    applications = ListField(ReferenceField('Application'))
    skill_sets = ListField(ReferenceField('SkillSet'))


class Application(Document):
    status = StringField(required=True)
    job_posting = ReferenceField(JobPosting)
    job_seeker = ReferenceField(JobSeeker)


class SkillSet(Document):
    skills = StringField(required=True)
    job_posting = ReferenceField(JobPosting)
