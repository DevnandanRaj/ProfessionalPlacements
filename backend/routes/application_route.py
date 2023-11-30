from flask import Blueprint, request, jsonify
from models.application import Application
from models.job_posting import JobPosting
from models.job_seeker import JobSeeker
from middleware.auth_middleware import auth_middleware

application_bp = Blueprint('application_bp', __name__)

# Apply to a job_posting by id 
@application_bp.route('/apply', methods=['POST'], endpoint='apply_to_job')
@auth_middleware(allowed_roles=['job_seeker'])
def apply_to_job():
    try:
        data = request.get_json()
        job_posting_id = data.get('job_posting_id')
        user_id = request.user['user_id']

        # Check if the job posting exists
        job_posting = JobPosting.objects(id=job_posting_id).first()
        if not job_posting:
            return jsonify({'message': 'Job posting not found'}), 404

        # Check if the job seeker exists
        job_seeker = JobSeeker.objects(user=user_id).first()
        if not job_seeker:
            return jsonify({'message': 'Job seeker not found'}), 404

        # Check if the job seeker has already applied to this job
        if Application.objects(job_seeker=job_seeker, job_posting=job_posting).first():
            return jsonify({'message': 'You have already applied to this job'}), 400

        # Create a new application
        application = Application(
            status='Pending',  # You can set the initial status to 'Pending'
            job_posting=job_posting,
            job_seeker=job_seeker
        )
        application.save()

        return jsonify({'message': 'Application submitted successfully'}), 201

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500


# Get all the application to jobs 
@application_bp.route('/get_applications', methods=['GET'], endpoint='get_job_applications')
@auth_middleware(allowed_roles=['job_seeker'])
def get_job_applications():
    try:
        user_id = request.user['user_id']

        # Check if the job seeker exists
        job_seeker = JobSeeker.objects(user=user_id).first()
        if not job_seeker:
            return jsonify({'message': 'Job seeker not found'}), 404

        # Get the list of applications for the job seeker
        applications = Application.objects(job_seeker=job_seeker)

        # Serialize the application data
        applications_data = [{
            'job_title': application.job_posting.job_title,
            'status': application.status,
            'applied_at': application.applied_at
        } for application in applications]

        return jsonify(applications_data), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500


# Update the status of an application by the hiring manager
@application_bp.route('/update_status/<application_id>', methods=['PUT'], endpoint='update_application_status')
@auth_middleware(allowed_roles=['hiring_manager'])
def update_application_status(application_id):
    try:
        data = request.get_json()
        new_status = data.get('new_status')

        # Check if the application exists
        application = Application.objects(id=application_id).first()
        if not application:
            return jsonify({'message': 'Application not found'}), 404

        # Check if the user updating the status is a hiring manager
        user_id = request.user['user_id']
        hiring_manager = application.job_posting.hiring_manager
        if hiring_manager.user.id != user_id:
            return jsonify({'message': 'You are not authorized to update the status of this application'}), 403

        # Update the status of the application
        application.status = new_status
        application.save()

        return jsonify({'message': 'Application status updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500
