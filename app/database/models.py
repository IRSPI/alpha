"""
NAME:          models.py
AUTHOR:        Alan Davies (Lecturer Health Data Science)
EMAIL:         alan.davies-2@manchester.ac.uk
DATE:          22/11/2019
INSTITUTION:   University of Manchester (FBMH)
DESCRIPTION:   Database ORM class
"""

from app import db, app
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Initialize password hashing

class User(db.Model, UserMixin):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        """Generate a secure reset token that expires in 30 minutes."""
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps(self.email, salt="password-reset-salt")

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """Verify the reset token and return the user."""
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt="password-reset-salt", max_age=expires_sec)
        except:
            return None
        return User.query.filter_by(email=email).first()

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

class PrescribingData(db.Model):
    """class for the prescription data table."""
    __tablename__ = 'practice_level_prescribing'
    id = db.Column(db.Integer, primary_key=True)
    SHA = db.Column(db.String(3))
    PCT = db.Column(db.String(3))
    practice = db.Column(db.String(6))
    BNF_code = db.Column("BNFCODE", db.String(15))
    BNF_name = db.Column("BNFNAME", db.String(40))
    items = db.Column(db.Integer)
    NIC = db.Column(db.Float)
    ACT_cost = db.Column("ACTCOST", db.Float)
    quantity = db.Column(db.Integer)

class PracticeData(db.Model):
    """Class for the practice address data table."""
    __tablename__ = 'practices'
    practice_code = db.Column(db.String(6), primary_key=True)
    practice_name = db.Column(db.Text)
    address_line_1 = db.Column(db.Text)
    address_line_2 = db.Column(db.Text)
    city = db.Column(db.Text)
    county = db.Column(db.Text)
    post_code = db.Column(db.String(10))



