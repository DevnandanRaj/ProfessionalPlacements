import datetime
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models.user import User

jwt = JWTManager()


def create_app(app):
    jwt.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.email

    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        return User.objects(email=identity).first()

    return app


def authenticate(email, password):
    user = User.objects(email=email).first()
    if user and user.check_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.objects(id=user_id).first()


@jwt_required()
def check_token():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

def generate_token(user):
    expires = datetime.timedelta(days=1)  # You can adjust the expiration time
    access_token = create_access_token(
        identity=str(user.id), expires_delta=expires)
    return access_token
