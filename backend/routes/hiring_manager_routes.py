from flask import Blueprint, request, jsonify
from models.hiring_manager import HiringManager
from middleware.auth_middleware import auth_middleware
from models.user import User
hiring_manager_bp = Blueprint('hiring_manager_bp', __name__)

# Route to update a hiring manager profile


@hiring_manager_bp.route('/updateProfile', methods=['PUT'], endpoint='update_hiring_manager_profile')
@auth_middleware(allowed_roles=['hiring_manager'])
def update_hiring_manager_profile():
    data = request.get_json()
    user_id = request.user['user_id']

    # Check if the user has a hiring manager profile
    hiring_manager = HiringManager.objects(user=user_id).first()
    if not hiring_manager:
        return jsonify({'message': 'Hiring manager profile not found'}), 404

    # Update hiring manager profile
    hiring_manager.name = data.get('name', hiring_manager.name)
    hiring_manager.current_jobrole = data.get(
        'current_jobrole', hiring_manager.current_jobrole)
    hiring_manager.company_description = data.get(
        'company_description', hiring_manager.company_description)
    hiring_manager.founded = data.get('founded', hiring_manager.founded)
    hiring_manager.website = data.get('website', hiring_manager.website)
    hiring_manager.company_size = data.get(
        'company_size', hiring_manager.company_size)
    hiring_manager.city = data.get('city', hiring_manager.city)
    hiring_manager.state = data.get('state', hiring_manager.state)
    hiring_manager.company_name = data.get(
        'company_name', hiring_manager.company_name)

    # Update email only if provided in the request data
    if 'email' in data:
        hiring_manager.email = data['email']

    # Update password only if provided in the request data
    if 'password' in data:
        hiring_manager.password = data['password']

    hiring_manager.save()

    # Update corresponding User model
    user = User.objects(id=hiring_manager.user.id).first()
    if user:
        # Update email only if provided in the request data
        if 'email' in data:
            user.email = data['email']

        # Update password only if provided in the request data
        if 'password' in data:
            user.password = data['password']

        user.save()
    return jsonify({'message': 'Hiring manager profile updated successfully'}), 200

# Route to delete a hiring manager profile


@hiring_manager_bp.route('/deleteProfile', methods=['DELETE'], endpoint='delete_hiring_manager_profile')
@auth_middleware(allowed_roles=['hiring_manager'])
def delete_hiring_manager_profile():
    user_id = request.user['user_id']

    # Check if the user has a hiring manager profile
    hiring_manager = HiringManager.objects(user=user_id).first()
    if not hiring_manager:
        return jsonify({'message': 'Hiring manager profile not found'}), 404

    # Delete hiring manager profile
    hiring_manager.delete()

    return jsonify({'message': 'Hiring manager profile deleted successfully'}), 200

# Route to get the details of the logged-in hiring manager


@hiring_manager_bp.route('/getProfile', methods=['GET'], endpoint='get_hiring_manager_profile')
@auth_middleware(allowed_roles=['hiring_manager'])
def get_hiring_manager_profile():
    user_id = request.user['user_id']

    # Check if the user has a hiring manager profile
    hiring_manager = HiringManager.objects(user=user_id).first()
    if not hiring_manager:
        return jsonify({'message': 'Hiring manager profile not found'}), 404

    # Serialize the hiring manager profile data
    profile_data = {
        'name': hiring_manager.name,
        'email': hiring_manager.email,
        'current_jobrole': hiring_manager.current_jobrole,
        'company_description': hiring_manager.company_description,
        'founded': hiring_manager.founded,
        'website': hiring_manager.website,
        'company_size': hiring_manager.company_size,
        'city': hiring_manager.city,
        'state': hiring_manager.state,
        'company_name': hiring_manager.company_name,
    }

    return jsonify(profile_data), 200
