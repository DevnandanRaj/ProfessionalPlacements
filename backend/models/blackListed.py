from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class RevokedToken(db.Document):
    token = db.StringField(unique=True)
    created_at = db.DateTimeField(default=datetime.utcnow)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        return cls.objects(jti=jti).first() is not None
