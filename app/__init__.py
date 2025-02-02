"""
NAME:          __init__.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          03/12/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Initialisation file. Creates the Flask application and SQL database
               registers the different modules in the project
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file



# Initialize Flask App
app = Flask(__name__)
app.config.from_object('config')

# Initialize Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Add email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')  # Load from environment
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')  # Load from environment
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')
# Debugging
print(f"Current Working Directory: {os.getcwd()}")  # Print where Flask is running from

load_dotenv()  # Load environment variables

print(f"Loaded EMAIL_USER: {os.getenv('EMAIL_USER')}")
print(f"Loaded EMAIL_PASS: {'*' * len(os.getenv('EMAIL_PASS')) if os.getenv('EMAIL_PASS') else 'Not Set'}")

mail = Mail(app)  # Initialize Flask-Mail

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Ensure this matches the correct blueprint

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.errorhandler(404)
def not_found(error):
    """Error page to show on page not found (404) error."""
    return render_template('404.html'), 404

# Import and register blueprints
from app.views.controllers import views as views_module, auth  # Import both dashboard and auth blueprints

app.register_blueprint(views_module)
app.register_blueprint(auth, url_prefix="/auth")  # Register authentication routes under `/auth`

@login_manager.user_loader
def load_user(user_id):
    from app.database.models import User  # Import the User model
    return User.query.get(int(user_id))



