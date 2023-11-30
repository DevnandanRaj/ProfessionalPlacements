import datetime
import jwt
import random
import string
from flask import Blueprint, request, jsonify, current_app 
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, HiringManager, JobSeeker
from models.blackListed import RevokedToken
from middleware.auth_middleware import auth_middleware
from flask_mail import Mail, Message
user_bp = Blueprint('user_bp', __name__)




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

# Route for forgot password


@user_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    user = User.objects(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    new_password = generate_random_password()
    hashed_password = generate_password_hash(new_password, method='sha256')

    user.password = hashed_password
    user.save()

    send_password_reset_email(user.email, new_password)

    return jsonify({'message': 'Password reset successful. Check your email for the new password.'}), 200

# Function to send a password reset email


def send_password_reset_email(email, new_password):
    from app import mail
    msg = Message('Password Reset',
                  sender='professionalplacements650@gmail.com', recipients=[email])
    msg.body = f'Your new password is: {new_password}, use this to login'

    # Send the email
    mail.send(msg)

# Function to generate a random password


def generate_random_password(length=12):
    # Ensure at least two symbols are included
    num_symbols = 2
    num_letters = length - num_symbols
    symbols = string.punctuation

    # Ensure at least one uppercase letter and one digit
    uppercase_letter = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)

    # Choose remaining letters and symbols
    remaining_letters = ''.join(random.choice(string.ascii_letters) for _ in range(num_letters - 2))
    remaining_symbols = ''.join(random.choice(symbols) for _ in range(num_symbols - 1))

    # Shuffle all the characters
    password_characters = list(uppercase_letter + digit + remaining_letters + remaining_symbols)
    random.shuffle(password_characters)

    return ''.join(password_characters)