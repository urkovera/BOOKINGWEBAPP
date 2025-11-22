from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from datetime import datetime
import re

main_bp = Blueprint('main', __name__)

# USER LOADER - This is the critical part!
@login_manager.user_loader
def load_user(username):
    """
    This function is called by Flask-Login to reload the user object
    from the user ID stored in the session.
    
    Args:
        username: The primary key (username/email) of the user
        
    Returns:
        User object or None if user doesn't exist
    """
    return User.query.get(username)
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        student_id = request.form.get('studentId', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        # Validation
        errors = []
        
        # 1. Check if all fields are provided
        if not all([first_name, last_name, student_id, email, password, confirm_password]):
            errors.append('All fields are required.')
        
        # 2. Validate email format and domain
        email_pattern = r'^[a-zA-Z0-9._%+-]+@mail\.kmutt\.ac\.th$'
        if email and not re.match(email_pattern, email):
            errors.append('Email must be a valid @mail.kmutt.ac.th address.')
        
        # 3. Validate student ID format (assuming 11 characters)
        if student_id and len(student_id) != 11:
            errors.append('Student ID must be 11 characters.')
        
        # 4. Check password length
        if password and len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        
        # 5. Check password match
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        # 6. Check if email already exists
        if email:
            existing_email = User.query.filter_by(username=email).first()
            if existing_email:
                errors.append('This email is already registered.')
        
        # 7. Check if student ID already exists
        if student_id:
            existing_student = User.query.filter_by(std_id=student_id).first()
            if existing_student:
                errors.append('This student ID is already registered.')
        
        # If there are validation errors, show them
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        try:
            # Create new user
            # Username will be the email
            full_name = f"{first_name} {last_name}"
            
            new_user = User(
                username=email,  # Using email as username
                name=full_name,
                role='Student',  # Default role for registration
                std_id=student_id,
                register_date=datetime.utcnow().date()
            )
            
            # Set password (will be hashed by the model method)
            new_user.set_password(password)
            
            # Add to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            print(f"Registration error: {str(e)}")  # For debugging
            return render_template('auth/register.html')
    
    # GET request - show registration form
    return render_template('auth/register.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        keep_logged_in = request.form.get('keepLoggedIn') == 'on'
        
        # Validation
        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('auth/login.html')
        
        # Find user by username (email)
        user = User.query.filter_by(username=email).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Log in the user
            login_user(user, remember=keep_logged_in)
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')
    
    # GET request - show login form
    return render_template('auth/login.html')


@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect('/login')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)