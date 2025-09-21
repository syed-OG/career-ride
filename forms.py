from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField, DateField, IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL, NumberRange, ValidationError
from datetime import date

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=64)])
    dob = DateField('Date of Birth', validators=[Optional()])
    bio = TextAreaField('About Me', validators=[Optional(), Length(max=500)])
    profile_picture = StringField('Profile Picture URL', validators=[Optional(), URL()])
    
    # Educational Information
    institution = StringField('Institution/University', validators=[Optional(), Length(max=128)])
    major = StringField('Major/Field of Study', validators=[Optional(), Length(max=128)])
    secondary_education = StringField('Secondary Education', validators=[Optional(), Length(max=256)])
    higher_education = StringField('Higher Education', validators=[Optional(), Length(max=256)])
    gpa = FloatField('GPA', validators=[Optional(), NumberRange(min=0, max=10)])
    credits_completed = IntegerField('Credits Completed', validators=[Optional(), NumberRange(min=0)])
    graduation_year = IntegerField('Expected Graduation Year', validators=[Optional()])
    
    # Career Information
    career_objective = TextAreaField('Career Objective', validators=[Optional(), Length(max=500)])
    areas_of_interest = TextAreaField('Areas of Interest (comma-separated)', validators=[Optional()])
    skills = TextAreaField('Skills (comma-separated)', validators=[Optional()])
    certifications = TextAreaField('Certifications', validators=[Optional()])
    languages_known = TextAreaField('Languages Known (comma-separated)', validators=[Optional()])
    
    # Extra Curricular
    achievements = TextAreaField('Achievements', validators=[Optional()])
    extracurricular_activities = TextAreaField('Extracurricular Activities', validators=[Optional()])
    
    # Social Links
    github_url = StringField('GitHub URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    portfolio_url = StringField('Portfolio URL', validators=[Optional(), URL()])
    twitter_url = StringField('Twitter URL', validators=[Optional(), URL()])
    instagram_url = StringField('Instagram URL', validators=[Optional(), URL()])
    
    submit = SubmitField('Update Profile')

    def validate_dob(self, dob):
        if dob.data and dob.data > date.today():
            raise ValidationError('Date of birth cannot be in the future')

class CareerGoalForm(FlaskForm):
    career_path_id = SelectField('Career Path', coerce=int, validators=[Optional()])
    custom_title = StringField('Custom Career Goal', validators=[Optional(), Length(max=128)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    target_date = DateField('Target Date', validators=[Optional()])
    submit = SubmitField('Save Goal')

    def validate_target_date(self, target_date):
        if target_date.data and target_date.data < date.today():
            raise ValidationError('Target date cannot be in the past')

class CodingSolutionForm(FlaskForm):
    language = SelectField('Language', choices=[
        ('python', 'Python'), 
        ('javascript', 'JavaScript'), 
        ('java', 'Java'), 
        ('cpp', 'C++')
    ])
    code = TextAreaField('Solution', validators=[DataRequired()])
    problem_id = HiddenField('Problem ID', validators=[DataRequired()])
    submit = SubmitField('Submit Solution')

class AIChatForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
