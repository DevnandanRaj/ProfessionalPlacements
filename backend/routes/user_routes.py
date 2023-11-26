
# routes/user_routes.py
import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, HiringManager, JobSeeker
from middleware.auth_middleware import authenticate, generate_token, check_token
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
            company_name =data['company_name']
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
        # User credentials are valid, generate a token
        access_token = generate_token(user)
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401



