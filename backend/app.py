# app.py

from routes.user_routes import user_bp
from flask import Flask
from flask_mongoengine import MongoEngine
from config import MONGODB_ATLAS_URI

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': MONGODB_ATLAS_URI,
    'connect': False  # Set to False to avoid automatic connection on app creation
}

db = MongoEngine(app)

# Import your user routes

# Register the user blueprint
app.register_blueprint(user_bp, url_prefix='/user')

print("Connected to MongoDB Atlas successfully!")

# Your other Flask-related configurations and routes go here

if __name__ == '__main__':
    app.run(debug=True)
