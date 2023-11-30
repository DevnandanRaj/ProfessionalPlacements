from flask import Blueprint, request, jsonify
from models.job_posting import JobPosting
from models.hiring_manager import HiringManager
from models.skill_set import SkillSet
from models.application import Application
from middleware.auth_middleware import auth_middleware

job_posting_bp = Blueprint('job_posting_bp', __name__)

# Route to create a new job posting


@job_posting_bp.route('/create', methods=['POST'], endpoint='create_job_posting')
@auth_middleware(allowed_roles=['hiring_manager'])
def create_job_posting():
    data = request.get_json()
    user_id = request.user['user_id']

    # Check if the user is a hiring manager
    hiring_manager = HiringManager.objects(user=user_id).first()
    if not hiring_manager:
        return jsonify({'message': 'You are not authorized to create a job posting'}), 403

    # Create SkillSet documents (if not already existing)
    skill_sets = []
    for skill_set_data in data.get('skill_sets', []):
        skill_set = SkillSet.objects(**skill_set_data).first()
        if not skill_set:
            skill_set = SkillSet(**skill_set_data)
            skill_set.save()
        skill_sets.append(skill_set)

    # Create a new job posting
    job_posting = JobPosting(
        job_title=data['job_title'],
        status=data['status'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        hiring_manager=hiring_manager,
        job_description=data['job_description'],
        salary=data['salary'],
        graduation=data['graduation'],
        postgraduation=data['postgraduation'],
        location=data['location'],
        role_category=data['role_category'],
        department=data['department'],
        experience=data['experience'],
        required_skills=data['required_skills'],
        prefered_skills=data['prefered_skills'],
        employment_type=data['employment_type'],
        openings=data['openings'],
        skill_sets=skill_sets
    )

    job_posting.save()

    return jsonify({'message': 'Job posting created successfully'}), 201


# Route to update a job posting


@job_posting_bp.route('/update/<job_posting_id>', methods=['PUT'], endpoint='update_job_posting')
@auth_middleware(allowed_roles=['hiring_manager'])
def update_job_posting(job_posting_id):
    data = request.get_json()
    user_id = request.user['user_id']

    # Check if the user is a hiring manager
    hiring_manager = HiringManager.objects(user=user_id).first()
    if not hiring_manager:
        return jsonify({'message': 'You are not authorized to update a job posting'}), 403

    # Check if the job posting exists
    job_posting = JobPosting.objects(
        id=job_posting_id, hiring_manager=hiring_manager).first()
    if not job_posting:
        return jsonify({'message': 'Job posting not found or you are not authorized to update it'}), 404

    # Update job posting
    job_posting.update(**data)

    return jsonify({'message': 'Job posting updated successfully'}), 200

# Route to delete a job posting


@job_posting_bp.route('/delete/<job_posting_id>', methods=['DELETE'], endpoint='delete_job_posting')
@auth_middleware(allowed_roles=['hiring_manager'])
def delete_job_posting(job_posting_id):
    user_id = request.user['user_id']

    # Check if the user is a hiring manager
    hiring_manager = HiringManager.objects(user=user_id).first()
    if not hiring_manager:
        return jsonify({'message': 'You are not authorized to delete a job posting'}), 403

    # Check if the job posting exists
    job_posting = JobPosting.objects(
        id=job_posting_id, hiring_manager=hiring_manager).first()
    if not job_posting:
        return jsonify({'message': 'Job posting not found or you are not authorized to delete it'}), 404

    # Delete job posting
    job_posting.delete()

    return jsonify({'message': 'Job posting deleted successfully'}), 200

# Route to get details of a job posting


@job_posting_bp.route('/get/<job_posting_id>', methods=['GET'], endpoint='get_job_posting')
def get_job_posting(job_posting_id):
    try:
        # Check if the job posting exists
        job_posting = JobPosting.objects(id=job_posting_id).first()
        if not job_posting:
            return jsonify({'message': 'Job posting not found'}), 404

        # Serialize the job posting data
        job_posting_data = {
            'job_title': job_posting.job_title,
            'status': job_posting.status,
            'start_date': job_posting.start_date,
            'end_date': job_posting.end_date,
            'hiring_manager': str(job_posting.hiring_manager.id),
            'job_description': job_posting.job_description,
            'salary': job_posting.salary,
            'graduation': job_posting.graduation,
            'postgraduation': job_posting.postgraduation,
            'location': job_posting.location,
            'role_category': job_posting.role_category,
            'department': job_posting.department,
            'experience': job_posting.experience,
            'required_skills': job_posting.required_skills,
            'prefered_skills': job_posting.prefered_skills,
            'employment_type': job_posting.employment_type,
            'openings': job_posting.openings,
            'timestamp': job_posting.timestamp,
            'applications': []
        }

        # Include information about applications for the job posting
        for application in job_posting.applications:
            applicant_data = {
                'applicant_name': application.job_seeker.name,
                'applicant_email': application.job_seeker.email,
                'applicant_skills': application.job_seeker.skills,
                'status': application.status,
                'applied_at': application.applied_at
            }
            job_posting_data['applications'].append(applicant_data)

        return jsonify(job_posting_data), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500

# Route to get all job postings


@job_posting_bp.route('/getAllJobs', methods=['GET'], endpoint='get_all_job_postings')
def get_all_job_postings():
    # Get all job postings
    job_postings = JobPosting.objects()

    # Serialize the job postings data
    job_postings_data = [{
        'job_title': job_posting.job_title,
        'status': job_posting.status,
        'start_date': job_posting.start_date,
        'end_date': job_posting.end_date,
        'hiring_manager': str(job_posting.hiring_manager.id),
        'job_description': job_posting.job_description,
        'salary': job_posting.salary,
        'graduation': job_posting.graduation,
        'postgraduation': job_posting.postgraduation,
        'location': job_posting.location,
        'role_category': job_posting.role_category,
        'department': job_posting.department,
        'experience': job_posting.experience,
        'required_skills': job_posting.required_skills,
        'prefered_skills': job_posting.prefered_skills,
        'employment_type': job_posting.employment_type,
        'openings': job_posting.openings,
        'timestamp': job_posting.timestamp
    } for job_posting in job_postings]

    return jsonify(job_postings_data), 200


# Route to get all job postings for the authenticated hiring manager
@job_posting_bp.route('/getJobsByManager', methods=['GET'], endpoint='get_all_job_postings_by_manager')
@auth_middleware(allowed_roles=['hiring_manager'])
def get_all_job_postings_by_manager():
    try:
        # Get the hiring manager's ID from the middleware
        hiring_manager_id = request.hiring_manager['user_id']

        # Check if the hiring manager exists
        hiring_manager = HiringManager.objects(id=hiring_manager_id).first()
        if not hiring_manager:
            return jsonify({'message': 'Hiring manager not found'}), 404

        # Get all job postings created by the hiring manager
        job_postings = JobPosting.objects(hiring_manager=hiring_manager)

        # Serialize the job postings data
        job_postings_data = [{
            'job_title': job_posting.job_title,
            'status': job_posting.status,
            'start_date': job_posting.start_date,
            'end_date': job_posting.end_date,
            'hiring_manager': str(job_posting.hiring_manager.id),
            'job_description': job_posting.job_description,
            'salary': job_posting.salary,
            'graduation': job_posting.graduation,
            'postgraduation': job_posting.postgraduation,
            'location': job_posting.location,
            'role_category': job_posting.role_category,
            'department': job_posting.department,
            'experience': job_posting.experience,
            'required_skills': job_posting.required_skills,
            'prefered_skills': job_posting.prefered_skills,
            'employment_type': job_posting.employment_type,
            'openings': job_posting.openings,
            'timestamp': job_posting.timestamp
        } for job_posting in job_postings]

        return jsonify(job_postings_data), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500
