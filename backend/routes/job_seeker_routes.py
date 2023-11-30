from flask import Blueprint, request, jsonify
from models.user import User
from models.job_seeker import JobSeeker, Degree
from middleware.auth_middleware import auth_middleware

jobseeker_bp = Blueprint('jobseeker_bp', __name__)

# Route to update a job seeker profile


@jobseeker_bp.route('/updateProfile', methods=['PUT'], endpoint='update_profile')
@auth_middleware(allowed_roles=['job_seeker'])
def update_jobseeker_profile():
    data = request.get_json()
    user_id = request.user['user_id']

    # Check if the user has a job seeker profile
    job_seeker = JobSeeker.objects(user=user_id).first()
    if not job_seeker:
        return jsonify({'message': 'Job seeker profile not found'}), 404

    # Update job seeker profile
    job_seeker.name = data.get('name', job_seeker.name)
    job_seeker.education = data.get('education', job_seeker.education)
    job_seeker.phone = data.get('phone', job_seeker.phone)
    job_seeker.address = data.get('address', job_seeker.address)
    job_seeker.city = data.get('city', job_seeker.city)
    job_seeker.state = data.get('state', job_seeker.state)
    job_seeker.pincode = data.get('pincode', job_seeker.pincode)
    job_seeker.status = data.get('status', job_seeker.status)
    job_seeker.skills = data.get('skills', job_seeker.skills)
    job_seeker.experience = data.get('experience', job_seeker.experience)
    job_seeker.bio = data.get('bio', job_seeker.bio)
    job_seeker.password = data.get('password', job_seeker.password)

    # Update degrees
    if 'degrees' in data:
        # Create and save Degree documents
        degrees = [Degree(**degree_data) for degree_data in data['degrees']]
        Degree.objects.insert(degrees)

        # Now assign the saved degrees to job_seeker
        job_seeker.degrees = degrees

    job_seeker.save()

    # Update email and password in the associated User model
    user = User.objects(id=job_seeker.user.id).first()
    if user:
        # Update email only if provided in the request data
        if 'email' in data:
            user.email = data['email']

        # Update password only if provided in the request data
        if 'password' in data:
            user.password = data['password']

        user.save()

    return jsonify({'message': 'Job seeker profile and user details updated successfully'}), 200

# Route to delete a job seeker profile


@jobseeker_bp.route('/deleteProfile', methods=['DELETE'], endpoint='delete_profile')
@auth_middleware(allowed_roles=['job_seeker'])
def delete_jobseeker_profile():
    user_id = request.user['user_id']

    # Check if the user has a job seeker profile
    job_seeker = JobSeeker.objects(user=user_id).first()
    if not job_seeker:
        return jsonify({'message': 'Job seeker profile not found'}), 404

    # Delete job seeker profile
    job_seeker.delete()

    return jsonify({'message': 'Job seeker profile deleted successfully'}), 200

# Route to get the details of the logged-in job seeker


@jobseeker_bp.route('/getProfile', methods=['GET'], endpoint='get_profile')
@auth_middleware(allowed_roles=['job_seeker'])
def get_jobseeker_profile():
    user_id = request.user['user_id']

    # Check if the user has a job seeker profile
    job_seeker = JobSeeker.objects(user=user_id).first()
    if not job_seeker:
        return jsonify({'message': 'Job seeker profile not found'}), 404

    # Serialize the job seeker profile data
    profile_data = {
        'name': job_seeker.name,
        'email': job_seeker.email,
        'education': job_seeker.education,
        'phone': job_seeker.phone,
        'address': job_seeker.address,
        'city': job_seeker.city,
        'state': job_seeker.state,
        'pincode': job_seeker.pincode,
        'status': job_seeker.status,
        'skills': job_seeker.skills,
        'experience': job_seeker.experience,
        'bio': job_seeker.bio,
        'degrees': [{'type': degree.type, 'college_name': degree.college_name, 'course_name': degree.course_name,
                     'marks': degree.marks, 'start_date': degree.start_date, 'end_date': degree.end_date}
                    for degree in job_seeker.degrees]
    }

    return jsonify(profile_data), 200
