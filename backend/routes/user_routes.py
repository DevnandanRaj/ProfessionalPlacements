import datetime
import jwt
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, HiringManager, JobSeeker
from models.blackListed import RevokedToken
from middleware.auth_middleware import auth_middleware

user_bp = Blueprint('user_bp', __name__)

# Route to register a new user (both job seekers and hiring managers)


@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Check if the email is already registered
    existing_user = User.objects(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # Create a new user
    new_user = User(
        email=data['email'],
        password=hashed_password,
        role=data['role'],
        created_at=datetime.datetime.utcnow()
    )
    new_user.save()

    # Create additional user-specific data (JobSeeker or HiringManager)
    if data['role'] == 'job_seeker':
        job_seeker = JobSeeker(
            user=new_user,
            name=data['name'],
            status=data['status'],
            skills=data['skills'],
            experience=data['experience'],
            bio=data['bio'],
        )
        job_seeker.save()
    elif data['role'] == 'hiring_manager':
        hiring_manager = HiringManager(
            user=new_user,
            name=data['name'],
            company_name=data['company_name']
            # Add other HiringManager fields as needed
        )
        hiring_manager.save()

    return jsonify({'message': 'User registered successfully'}), 201

# Route to log in a user


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.objects(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        # Include role information in the token
        role_info = {
            'user_id': str(user.id),
            'role': user.role,  # Assuming the user model has a 'role' field
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(
            role_info, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
        return jsonify({'token': token, "msg": f"Welcome {user.role}"}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
# Route to log out a user


@user_bp.route('/logout', methods=['POST'])
@auth_middleware(allowed_roles=['job_seeker', 'hiring_manager'])
def logout_user():
    try:
        token = request.headers.get('Authorization')
        # Check if the token is already revoked
        if not RevokedToken.objects(token=token):
            RevokedToken(token=token).save()
            return jsonify({'message': 'Logged out successfully'}), 200
        else:
            return jsonify({'message': 'Token already revoked'}), 400

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
