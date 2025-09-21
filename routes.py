import json
import os
from flask import render_template, url_for, flash, redirect, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime, date
from app import db
from models import (
    User, Profile, Course, Enrollment, CareerPath, CareerGoal, 
    CodingProblem, CodingSolution, AptitudeTest, AptitudeQuestion, 
    AptitudeTestResult, AiChatMessage
)
from forms import (
    RegistrationForm, LoginForm, ProfileForm, CareerGoalForm, 
    CodingSolutionForm, AIChatForm, ResetPasswordRequestForm, ResetPasswordForm
)
from utils import (
    get_career_match_score, parse_json_string, format_datetime, 
    evaluate_code_solution, get_coding_problems_sample_data,
    get_aptitude_test_sample_data, get_career_paths_sample_data,
    get_ai_advisor_response
)

def configure_routes(app):
    
    @app.route('/')
    def index():
        return render_template('index.html', title='Home')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = RegistrationForm()
        if form.validate_on_submit():
            # Check if username or email already exists
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken. Please choose a different one.', 'danger')
                return render_template('register.html', title='Register', form=form)
            
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('Email already registered. Please use a different one or login.', 'danger')
                return render_template('register.html', title='Register', form=form)
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            # Create empty profile
            profile = Profile(user=user)
            
            db.session.add(user)
            db.session.add(profile)
            db.session.commit()
            
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html', title='Register', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
        
        return render_template('login.html', title='Login', form=form)
    
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Get user profile data
        profile = current_user.profile
        
        # Get career goals
        career_goals = CareerGoal.query.filter_by(user_id=current_user.id).all()
        
        # Get recent aptitude test results
        test_results = AptitudeTestResult.query.filter_by(user_id=current_user.id).order_by(AptitudeTestResult.completed_at.desc()).limit(3).all()
        
        # Get recent coding activities
        coding_solutions = CodingSolution.query.filter_by(user_id=current_user.id).order_by(CodingSolution.submitted_at.desc()).limit(3).all()
        
        # For a new application, let's populate with sample data if DB is empty
        initialize_sample_data_if_needed()
        
        return render_template(
            'dashboard.html', 
            title='Dashboard',
            profile=profile,
            career_goals=career_goals,
            test_results=test_results,
            coding_solutions=coding_solutions
        )
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm()
        
        if form.validate_on_submit():
            # Update user data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.dob = form.dob.data
            current_user.institution = form.institution.data
            current_user.major = form.major.data
            current_user.bio = form.bio.data
            
            # Update profile data
            if not current_user.profile:
                current_user.profile = Profile(user_id=current_user.id)
            
            # Update basic profile fields
            current_user.profile.gpa = form.gpa.data
            current_user.profile.credits_completed = form.credits_completed.data
            current_user.profile.graduation_year = form.graduation_year.data
            current_user.profile.skills = form.skills.data
            current_user.profile.achievements = form.achievements.data
            
            # Update additional profile info
            current_user.profile.areas_of_interest = form.areas_of_interest.data
            current_user.profile.career_objective = form.career_objective.data
            current_user.profile.extracurricular_activities = form.extracurricular_activities.data
            current_user.profile.certifications = form.certifications.data
            current_user.profile.secondary_education = form.secondary_education.data
            current_user.profile.higher_education = form.higher_education.data
            current_user.profile.languages_known = form.languages_known.data
            current_user.profile.profile_picture = form.profile_picture.data
            
            # Update social links
            current_user.profile.github_url = form.github_url.data
            current_user.profile.linkedin_url = form.linkedin_url.data
            current_user.profile.portfolio_url = form.portfolio_url.data
            current_user.profile.twitter_url = form.twitter_url.data
            current_user.profile.instagram_url = form.instagram_url.data
            
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile'))
        
        elif request.method == 'GET':
            # Populate form with existing data
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.dob.data = current_user.dob
            form.institution.data = current_user.institution
            form.major.data = current_user.major
            form.bio.data = current_user.bio
            
            if current_user.profile:
                # Basic profile data
                form.gpa.data = current_user.profile.gpa
                form.credits_completed.data = current_user.profile.credits_completed
                form.graduation_year.data = current_user.profile.graduation_year
                form.skills.data = current_user.profile.skills
                form.achievements.data = current_user.profile.achievements
                
                # Additional profile data
                form.areas_of_interest.data = current_user.profile.areas_of_interest
                form.career_objective.data = current_user.profile.career_objective
                form.extracurricular_activities.data = current_user.profile.extracurricular_activities
                form.certifications.data = current_user.profile.certifications
                form.secondary_education.data = current_user.profile.secondary_education
                form.higher_education.data = current_user.profile.higher_education
                form.languages_known.data = current_user.profile.languages_known
                form.profile_picture.data = current_user.profile.profile_picture
                
                # Social links
                form.github_url.data = current_user.profile.github_url
                form.linkedin_url.data = current_user.profile.linkedin_url
                form.portfolio_url.data = current_user.profile.portfolio_url
                form.twitter_url.data = current_user.profile.twitter_url
                form.instagram_url.data = current_user.profile.instagram_url
        
        return render_template('profile.html', title='Profile', form=form)
    
    @app.route('/courses')
    @login_required
    def courses():
        # Get all courses
        course_query = Course.query
        
        # Apply filters if provided
        search = request.args.get('search', '')
        department = request.args.get('department', '')
        level = request.args.get('level', '')
        
        if search:
            course_query = course_query.filter(
                (Course.title.contains(search)) | 
                (Course.code.contains(search)) | 
                (Course.description.contains(search))
            )
        
        if department:
            course_query = course_query.filter_by(department=department)
            
        if level:
            course_query = course_query.filter_by(level=level)
        
        # Get user enrollments for display
        user_enrollments = {e.course_id: e for e in current_user.enrollments}
        
        courses = course_query.all()
        return render_template(
            'courses.html', 
            title='Courses',
            courses=courses,
            user_enrollments=user_enrollments,
            search=search,
            department=department,
            level=level
        )
    
    @app.route('/career-paths')
    @login_required
    def career_paths():
        career_paths = CareerPath.query.all()
        
        # Calculate match scores if user has skills
        match_scores = {}
        if current_user.profile and current_user.profile.skills:
            for path in career_paths:
                match_scores[path.id] = get_career_match_score(
                    current_user.profile.skills, 
                    path.required_skills
                )
        
        return render_template(
            'career_paths.html', 
            title='Career Paths',
            career_paths=career_paths,
            match_scores=match_scores
        )
    
    @app.route('/career-goal/new', methods=['GET', 'POST'])
    @login_required
    def new_career_goal():
        form = CareerGoalForm()
        
        # Populate career path choices
        career_paths = CareerPath.query.all()
        form.career_path_id.choices = [(0, 'Custom Goal')] + [(path.id, path.name) for path in career_paths]
        
        if form.validate_on_submit():
            career_goal = CareerGoal(
                user_id=current_user.id,
                custom_title=form.custom_title.data,
                description=form.description.data,
                target_date=form.target_date.data,
                progress=0  # Start at 0%
            )
            
            # Link to career path if selected
            if form.career_path_id.data > 0:
                career_goal.career_path_id = form.career_path_id.data
            
            db.session.add(career_goal)
            db.session.commit()
            
            flash('Career goal added successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        return render_template('career_goal_form.html', title='New Career Goal', form=form)
    
    @app.route('/career-goal/<int:goal_id>/update', methods=['GET', 'POST'])
    @login_required
    def update_career_goal(goal_id):
        career_goal = CareerGoal.query.get_or_404(goal_id)
        
        # Check if the goal belongs to the current user
        if career_goal.user_id != current_user.id:
            flash('You do not have permission to edit this goal.', 'danger')
            return redirect(url_for('dashboard'))
        
        form = CareerGoalForm()
        
        # Populate career path choices
        career_paths = CareerPath.query.all()
        form.career_path_id.choices = [(0, 'Custom Goal')] + [(path.id, path.name) for path in career_paths]
        
        if form.validate_on_submit():
            if form.career_path_id.data > 0:
                career_goal.career_path_id = form.career_path_id.data
            else:
                career_goal.career_path_id = None
                
            career_goal.custom_title = form.custom_title.data
            career_goal.description = form.description.data
            career_goal.target_date = form.target_date.data
            
            db.session.commit()
            flash('Career goal updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        elif request.method == 'GET':
            form.career_path_id.data = career_goal.career_path_id or 0
            form.custom_title.data = career_goal.custom_title
            form.description.data = career_goal.description
            form.target_date.data = career_goal.target_date
        
        return render_template('career_goal_form.html', title='Update Career Goal', form=form)
    
    @app.route('/coding-practice')
    @login_required
    def coding_practice():
        # Get all coding problems
        problem_query = CodingProblem.query
        
        # Apply filters if provided
        difficulty = request.args.get('difficulty', '')
        topic = request.args.get('topic', '')
        status = request.args.get('status', '')
        
        if difficulty:
            problem_query = problem_query.filter_by(difficulty=difficulty)
            
        if topic:
            problem_query = problem_query.filter_by(topic=topic)
        
        problems = problem_query.all()
        
        # Get user solutions for display
        user_solutions = {s.problem_id: s for s in CodingSolution.query.filter_by(user_id=current_user.id).all()}
        
        # Filter by status if requested
        if status == 'solved':
            problems = [p for p in problems if p.id in user_solutions and user_solutions[p.id].status == 'Accepted']
        elif status == 'attempted':
            problems = [p for p in problems if p.id in user_solutions]
        elif status == 'unsolved':
            problems = [p for p in problems if p.id not in user_solutions]
        
        return render_template(
            'coding_practice.html', 
            title='Coding Practice',
            problems=problems,
            user_solutions=user_solutions,
            difficulty=difficulty,
            topic=topic,
            status=status
        )
    
    @app.route('/problem/<int:problem_id>')
    @login_required
    def view_problem(problem_id):
        problem = CodingProblem.query.get_or_404(problem_id)
        form = CodingSolutionForm()
        form.problem_id.data = problem_id
        
        # Get user's previous solutions to this problem
        previous_solutions = CodingSolution.query.filter_by(
            user_id=current_user.id, 
            problem_id=problem_id
        ).order_by(CodingSolution.submitted_at.desc()).all()
        
        return render_template(
            'code_editor.html',
            title=f'Problem: {problem.title}',
            problem=problem,
            form=form,
            previous_solutions=previous_solutions
        )
    
    @app.route('/submit-solution', methods=['POST'])
    @login_required
    def submit_solution():
        form = CodingSolutionForm()
        
        if form.validate_on_submit():
            problem_id = form.problem_id.data
            problem = CodingProblem.query.get_or_404(problem_id)
            
            # Evaluate the submitted code
            result = evaluate_code_solution(
                problem=problem,
                code=form.code.data,
                language=form.language.data
            )
            
            # Save the solution
            solution = CodingSolution(
                user_id=current_user.id,
                problem_id=problem_id,
                language=form.language.data,
                code=form.code.data,
                status=result['status'],
                runtime=result['runtime'],
                memory_used=result['memory_used']
            )
            
            db.session.add(solution)
            db.session.commit()
            
            flash(f'Solution submitted! Status: {result["status"]}', 'info')
            return redirect(url_for('view_problem', problem_id=problem_id))
        
        flash('There was an error with your submission.', 'danger')
        return redirect(url_for('coding_practice'))
    
    @app.route('/aptitude-tests')
    @login_required
    def aptitude_tests():
        # Get all aptitude tests
        tests = AptitudeTest.query.all()
        
        # Get user's test results
        user_results = {}
        for result in AptitudeTestResult.query.filter_by(user_id=current_user.id).all():
            user_results[result.test_id] = result
        
        return render_template(
            'aptitude_tests.html', 
            title='Aptitude Tests',
            tests=tests,
            user_results=user_results
        )
    
    @app.route('/take-test/<int:test_id>')
    @login_required
    def take_test(test_id):
        test = AptitudeTest.query.get_or_404(test_id)
        questions = AptitudeQuestion.query.filter_by(test_id=test_id).all()
        
        return render_template(
            'test_taking.html',
            title=f'Test: {test.category}',
            test=test,
            questions=questions
        )
    
    @app.route('/submit-test/<int:test_id>', methods=['POST'])
    @login_required
    def submit_test(test_id):
        test = AptitudeTest.query.get_or_404(test_id)
        questions = AptitudeQuestion.query.filter_by(test_id=test_id).all()
        
        # Process answers
        answers = {}
        score = 0
        
        for question in questions:
            selected_option = request.form.get(f'q{question.id}')
            if selected_option:
                answer_index = int(selected_option)
                answers[question.id] = answer_index
                
                # Check if answer is correct
                if answer_index == question.correct_option:
                    score += 1
        
        # Calculate score percentage
        score_percentage = (score / len(questions)) * 100 if questions else 0
        
        # Save test result
        test_result = AptitudeTestResult(
            user_id=current_user.id,
            test_id=test_id,
            score=score,
            score_percentage=score_percentage,
            answers=json.dumps(answers),
            time_taken=request.form.get('time_taken', 0)
        )
        
        db.session.add(test_result)
        db.session.commit()
        
        flash(f'Test submitted! Your score: {score}/{len(questions)} ({score_percentage:.1f}%)', 'info')
        return redirect(url_for('test_results', result_id=test_result.id))
    
    @app.route('/test-results/<int:result_id>')
    @login_required
    def test_results(result_id):
        result = AptitudeTestResult.query.get_or_404(result_id)
        
        # Check if the result belongs to the current user
        if result.user_id != current_user.id:
            flash('You do not have permission to view these results.', 'danger')
            return redirect(url_for('aptitude_tests'))
        
        test = result.test
        questions = AptitudeQuestion.query.filter_by(test_id=test.id).all()
        
        # Parse answers
        answers = parse_json_string(result.answers)
        
        return render_template(
            'test_results.html',
            title='Test Results',
            result=result,
            test=test,
            questions=questions,
            answers=answers
        )
    
    @app.route('/ai-advisor', methods=['GET', 'POST'])
    @login_required
    def ai_advisor():
        form = AIChatForm()
        
        if form.validate_on_submit():
            # Save user message
            user_message = AiChatMessage(
                user_id=current_user.id,
                is_user=True,
                message=form.message.data
            )
            db.session.add(user_message)
            
            # Generate AI response
            response_text = get_ai_advisor_response(
                user_message=form.message.data,
                user_profile=current_user.profile
            )
            
            # Save AI response
            ai_response = AiChatMessage(
                user_id=current_user.id,
                is_user=False,
                message=response_text
            )
            db.session.add(ai_response)
            db.session.commit()
            
            return redirect(url_for('ai_advisor'))
        
        # Get conversation history
        messages = AiChatMessage.query.filter_by(user_id=current_user.id).order_by(AiChatMessage.created_at).all()
        
        return render_template(
            'ai_advisor.html',
            title='AI Advisor',
            form=form,
            messages=messages
        )
    
    @app.route('/reset-password-request', methods=['GET', 'POST'])
    def reset_password_request():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        form = ResetPasswordRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                token = user.get_reset_token()
                # In a real application, you would send an email with reset_url
                # reset_url = url_for('reset_password', token=token, _external=True)
                
                # For the sake of demonstration, we'll show the token on screen
                flash(f'Password reset token: {token}', 'info')
                flash('A password reset link would normally be sent to your email', 'info')
            else:
                # We don't reveal if an email exists in the system for security
                pass
            
            flash('If your email is registered, you will receive password reset instructions.', 'info')
            return redirect(url_for('login'))
            
        return render_template('reset_password_request.html', title='Reset Password', form=form)
    
    @app.route('/reset-password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        user = User.verify_reset_token_static(token)
        if not user:
            flash('Invalid or expired reset token', 'warning')
            return redirect(url_for('reset_password_request'))
        
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            user.clear_reset_token()
            db.session.commit()
            flash('Your password has been updated! You can now login.', 'success')
            return redirect(url_for('login'))
            
        return render_template('reset_password.html', title='Reset Password', form=form)
    
    @app.route('/developer-roadmaps')
    @login_required
    def developer_roadmaps():
        # Get career paths as roadmaps
        roadmaps = CareerPath.query.all()
        
        return render_template(
            'developer_roadmaps.html',
            title='Developer Roadmaps',
            roadmaps=roadmaps
        )
        
    def initialize_sample_data_if_needed():
        """Initialize the database with sample data if it's empty."""
        # Check if we already have data
        if CareerPath.query.first() is not None:
            return
            
        # Add career paths
        for path_data in get_career_paths_sample_data():
            path = CareerPath(**path_data)
            db.session.add(path)
        
        # Add coding problems
        for problem_data in get_coding_problems_sample_data():
            problem = CodingProblem(**problem_data)
            db.session.add(problem)
        
        # Add aptitude tests
        aptitude_data = get_aptitude_test_sample_data()
        
        for category, test_data in aptitude_data.items():
            test = AptitudeTest(
                category=category.replace('_', ' ').title(),
                description=test_data['description'],
                total_questions=test_data['total_questions'],
                time_limit=test_data['time_limit'],
                passing_score=test_data['passing_score']
            )
            db.session.add(test)
            db.session.flush()  # Get test ID
            
            # Add questions for this test
            for q_data in test_data['questions']:
                question = AptitudeQuestion(
                    test_id=test.id,
                    question_text=q_data['question_text'],
                    options=json.dumps(q_data['options']),
                    correct_option=q_data['correct_option'],
                    explanation=q_data['explanation']
                )
                db.session.add(question)
        
        db.session.commit()
