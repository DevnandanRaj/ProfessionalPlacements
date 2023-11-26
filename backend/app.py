# app.py

from routes.user_routes import user_bp
from flask import Flask
from flask_mongoengine import MongoEngine
from config import MONGODB_ATLAS_URI, JWT_SECRET_KEY
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': MONGODB_ATLAS_URI,
    'connect': False  # Set to False to avoid automatic connection on app creation
}
jwt = JWTManager(app)
# Replace with your actual secret key
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
db = MongoEngine(app)

# Import your user routes

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')

print("Connected to MongoDB Atlas successfully!")

# Your other Flask-related configurations and routes go here

if __name__ == '__main__':
    app.run(debug=True)
