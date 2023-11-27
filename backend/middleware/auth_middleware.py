# middleware/auth_middleware.py
import jwt
from flask import request, jsonify, current_app
from models.blackListed import RevokedToken


def auth_middleware(allowed_roles=None):
    def middleware_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if not token:
                    return jsonify({'message': 'Authorization token not found'}), 401

                # Check if the token is blacklisted
                is_blacklisted = RevokedToken.objects(token=token).first()
                if is_blacklisted:
                    return jsonify({'message': 'Token revoked. Please login again.'}), 401

                # Verify the access token
                decoded = jwt.decode(
                    token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                user_id = decoded['user_id']
                user_role = decoded.get('role', None)

                # Check if the user has the required role for specific routes
                if allowed_roles is not None and user_role not in allowed_roles:
                    return jsonify({'message': 'Insufficient permissions to access this resource'}), 403

                request.user = {'user_id': user_id, 'role': user_role}
                return func(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401

        return wrapper

    return middleware_decorator
