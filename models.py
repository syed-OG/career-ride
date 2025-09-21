from datetime import datetime, timedelta
import os
import secrets
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    dob = db.Column(db.Date)
    institution = db.Column(db.String(128))
    major = db.Column(db.String(128))
    bio = db.Column(db.Text)
    reset_token = db.Column(db.String(100))
    reset_token_expiration = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade="all, delete-orphan")
    career_goals = db.relationship('CareerGoal', backref='user', lazy=True, cascade="all, delete-orphan")
    aptitude_tests = db.relationship('AptitudeTestResult', backref='user', lazy=True, cascade="all, delete-orphan")
    coding_solutions = db.relationship('CodingSolution', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def get_reset_token(self, expires_in=3600):
        """Generate a password reset token that expires in 1 hour by default"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiration = datetime.utcnow() + timedelta(seconds=expires_in)
        db.session.commit()
        return self.reset_token
        
    def verify_reset_token(self, token):
        """Verify if the reset token is valid and not expired"""
        if self.reset_token != token or self.reset_token_expiration < datetime.utcnow():
            return False
        return True
        
    @staticmethod
    def verify_reset_token_static(token):
        """Static method to find user by token"""
        user = User.query.filter_by(reset_token=token).first()
        if user is None or user.reset_token_expiration < datetime.utcnow():
            return None
        return user
    
    def clear_reset_token(self):
        """Clear the reset token after it has been used"""
        self.reset_token = None
        self.reset_token_expiration = None
        db.session.commit()

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gpa = db.Column(db.Float)
    credits_completed = db.Column(db.Integer, default=0)
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.Text)  # Stored as comma-separated values
    achievements = db.Column(db.Text)  # Stored as JSON string
    areas_of_interest = db.Column(db.Text)  # Stored as comma-separated values
    career_objective = db.Column(db.Text)
    extracurricular_activities = db.Column(db.Text)
    certifications = db.Column(db.Text)  # Stored as JSON string
    secondary_education = db.Column(db.String(256))
    higher_education = db.Column(db.String(256))
    languages_known = db.Column(db.Text)  # Stored as comma-separated values
    github_url = db.Column(db.String(128))
    linkedin_url = db.Column(db.String(128))
    portfolio_url = db.Column(db.String(128))
    twitter_url = db.Column(db.String(128))
    instagram_url = db.Column(db.String(128))
    profile_picture = db.Column(db.String(256))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, default=3)
    prerequisites = db.Column(db.Text)  # Stored as comma-separated course codes
    department = db.Column(db.String(64))
    level = db.Column(db.String(32))  # e.g., "Undergraduate", "Graduate"
    is_nptel = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade="all, delete-orphan")

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    status = db.Column(db.String(32), default="Enrolled")  # "Enrolled", "Completed", "In Progress"
    grade = db.Column(db.String(2))
    completed_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='enrollments')

class CareerPath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)  # Stored as comma-separated values
    recommended_courses = db.Column(db.Text)  # Stored as comma-separated course IDs
    job_outlook = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CareerGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    career_path_id = db.Column(db.Integer, db.ForeignKey('career_path.id'))
    custom_title = db.Column(db.String(128))
    description = db.Column(db.Text)
    target_date = db.Column(db.Date)
    progress = db.Column(db.Integer, default=0)  # Percentage from 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    career_path = db.relationship('CareerPath')

class CodingProblem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(16))  # "Easy", "Medium", "Hard"
    topic = db.Column(db.String(64))
    example_input = db.Column(db.Text)
    example_output = db.Column(db.Text)
    test_cases = db.Column(db.Text)  # Stored as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    solutions = db.relationship('CodingSolution', backref='problem', lazy=True)

class CodingSolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problem.id'), nullable=False)
    language = db.Column(db.String(32))  # "Python", "JavaScript", etc.
    code = db.Column(db.Text)
    status = db.Column(db.String(16))  # "Accepted", "Wrong Answer", "Runtime Error", etc.
    runtime = db.Column(db.Integer)  # in milliseconds
    memory_used = db.Column(db.Integer)  # in KB
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class AptitudeTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable=False)  # "Logical Reasoning", "Verbal Ability", etc.
    description = db.Column(db.Text)
    total_questions = db.Column(db.Integer, default=0)
    time_limit = db.Column(db.Integer)  # in minutes, NULL for no limit
    passing_score = db.Column(db.Integer)  # percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('AptitudeQuestion', backref='test', lazy=True, cascade="all, delete-orphan")

class AptitudeQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('aptitude_test.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)  # Stored as JSON array
    correct_option = db.Column(db.Integer)
    explanation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AptitudeTestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('aptitude_test.id'), nullable=False)
    score = db.Column(db.Integer)  # total correct answers
    score_percentage = db.Column(db.Float)  # percentage score
    answers = db.Column(db.Text)  # JSON of question_id: selected_option
    time_taken = db.Column(db.Integer)  # in seconds
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    test = db.relationship('AptitudeTest')

class AiChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_user = db.Column(db.Boolean, default=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='ai_chat_messages')
