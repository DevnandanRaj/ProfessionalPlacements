from flask import Blueprint, jsonify
from models.skill_set import SkillSet, Job
from models.job_posting import JobPosting 
from mongoengine import DoesNotExist

skill_set_bp = Blueprint('skill_set_bp', __name__)

# Function to generate jobs from skill sets


def generate_jobs_from_skill_sets(job_postings, skill_set):
    job_titles = []
    for job_posting in job_postings:
        job = Job(
            job_title=f"{job_posting.job_title} - {skill_set.skills} Specialist",
            status='Active',
            start_date=job_posting.start_date,
            end_date=job_posting.end_date,
            hiring_manager=job_posting.hiring_manager,
            job_description=job_posting.job_description,
            salary=job_posting.salary,
            graduation=job_posting.graduation,
            postgraduation=job_posting.postgraduation,
            location=job_posting.location,
            role_category=job_posting.role_category,
            department=job_posting.department,
            experience=job_posting.experience,
            required_skills=job_posting.required_skills,
            prefered_skills=skill_set.skills,
            employment_type=job_posting.employment_type,
            openings=job_posting.openings,
            timestamp=job_posting.timestamp
        )
        skill_set.jobs.append(job)
        skill_set.save()
        job_titles.append(job.job_title)
    return job_titles

# Route to automatically create job collections based on job postings' preferred skills


@skill_set_bp.route('/create_job_collections', methods=['POST'], endpoint='create_job_collections')
def create_job_collections():
    try:
        # Find all unique preferred skills from existing job postings
        unique_preferred_skills = JobPosting.objects.distinct(
            "prefered_skills")

        # Check if there are preferred skills to create a SkillSet
        if not unique_preferred_skills:
            return jsonify({'message': 'No preferred skills found'}), 404

        # Create a new skill set
        skill_set = SkillSet(skills=unique_preferred_skills)
        skill_set.save()

        # Find job postings with the specified skills
        job_postings = JobPosting.objects(
            prefered_skills__in=unique_preferred_skills)

        # Generate job collections based on the job postings with preferred skills
        job_titles = generate_jobs_from_skill_sets(job_postings, skill_set)

        return jsonify({'message': 'Job collections created successfully', 'job_titles': job_titles}), 201

    except DoesNotExist as e:
        return jsonify({'message': 'Error: Job postings or skill set not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error processing the request: {str(e)}'}), 500

# Route to get all skill sets and related jobs


@skill_set_bp.route('/get_all_skill_sets', methods=['GET'], endpoint='get_all_skill_sets')
def get_all_skill_sets():
    try:
        # Get all skill sets
        skill_sets = SkillSet.objects()

        # Serialize the skill sets data along with related jobs
        skill_sets_data = []
        for skill_set in skill_sets:
            jobs_data = skill_set.jobs
            skill_set_data = {
                'skills': skill_set.skills,
                'jobs': jobs_data
            }
            skill_sets_data.append(skill_set_data)

        return jsonify(skill_sets_data), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500

# Route to get skill set by ID


@skill_set_bp.route('/get_skill_set/<skill_set_id>', methods=['GET'], endpoint='get_skill_set_by_id')
def get_skill_set_by_id(skill_set_id):
    try:
        # Get skill set by ID
        skill_set = SkillSet.objects(id=skill_set_id).first()

        # Check if the skill set exists
        if not skill_set:
            return jsonify({'message': 'Skill set not found'}), 404

        # Serialize the skill set data along with related jobs
        jobs_data = skill_set.jobs
        skill_set_data = {
            'skills': skill_set.skills,
            'jobs': jobs_data
        }

        return jsonify(skill_set_data), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500

# Route to delete a skill set by ID


@skill_set_bp.route('/delete_skill_set/<skill_set_id>', methods=['DELETE'], endpoint='delete_skill_set_by_id')
def delete_skill_set_by_id(skill_set_id):
    try:
        # Get skill set by ID
        skill_set = SkillSet.objects(id=skill_set_id).first()

        # Check if the skill set exists
        if not skill_set:
            return jsonify({'message': 'Skill set not found'}), 404

        # Delete the skill set
        skill_set.delete()

        return jsonify({'message': 'Skill set deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Error processing the request'}), 500
