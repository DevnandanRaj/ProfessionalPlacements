from flask import Flask
from flask_mongoengine import MongoEngine
from config import MONGODB_ATLAS_URI, JWT_SECRET_KEY, JWT_ALGORITHM, MAIL_DEFAULT_SENDER, MAIL_PASSWORD, MAIL_USERNAME
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from routes.user_routes import user_bp
from routes.job_seeker_routes import jobseeker_bp
from routes.hiring_manager_routes import hiring_manager_bp
from routes.job_posting_routes import job_posting_bp
from routes.application_route import application_bp 
from routes.skill_set_route import skill_set_bp
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': MONGODB_ATLAS_URI,
    'connect': False  # Set to False to avoid automatic connection on app creation
}
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ALGORITHM'] = JWT_ALGORITHM
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
db = MongoEngine(app)

# Initialize Flask-Mail
mail = Mail()
mail.init_app(app)

# Register user routes with URL prefix
app.register_blueprint(user_bp, url_prefix='/user')
# Register jobseeker routes with URL prefix
app.register_blueprint(jobseeker_bp, url_prefix='/jobseeker')
# Register hiring manager routes with URL prefix
app.register_blueprint(hiring_manager_bp, url_prefix='/hiring_manager')
# Register job posting routes with URL prefix
app.register_blueprint(job_posting_bp, url_prefix='/job_posting')
# Register application routes with URL prefix
app.register_blueprint(application_bp, url_prefix='/application')
# Register skill set routes with URL prefix
app.register_blueprint(skill_set_bp, url_prefix='/skill_set')

print("Connected to MongoDB Atlas successfully!")

# Your other Flask-related configurations and routes go here

if __name__ == '__main__':
    app.run(debug=True)
