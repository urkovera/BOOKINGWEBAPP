from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from datetime import datetime
import re

main_bp = Blueprint('main', __name__)

# --- REQUIRED: User Loader for Flask-Login ---
# This is crucial! It tells Flask-Login how to find a user from a session cookie.
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

# --- ROUTE 1: Root URL (Redirects based on login status) ---
@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # Change this to redirect to 'home' page (landing page) if you have one, 
    # or 'login' if you want to force login immediately.
    # Based on your templates, you seem to have a landing page at main.home? 
    # If main.home IS the dashboard, then redirecting to login here is correct for guests.
    return redirect(url_for('main.login'))

# --- ROUTE 2: Home Page (The Dashboard) ---
@main_bp.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user) 

# --- ROUTE 3: Login ---
@main_bp.route('/login', methods=['GET', 'POST'])
def login(): 
    # If user is already logged in, send them home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
       
    if request.method == 'POST':
        # Get data from form
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '') 
        
        # CHECKBOX LOGIC: 
        # HTML sends 'on' if checked, or None if unchecked.
        keep_logged_in = request.form.get('keepLoggedIn') == 'on'
        
        user = User.query.filter_by(username=email).first()
        
        if user and user.check_password(password):    
            # PASS REMEMBER=TRUE TO ENABLE THE LONG-LIVED TOKEN
            login_user(user, remember=keep_logged_in)
            
            flash(f'Welcome back, {user.name}!', 'success')
            
            # Redirect to next page if it exists (e.g. user tried to access unauthorized page)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.home'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('auth/login.html')

# --- ROUTE 4: Logout ---
@main_bp.route('/logout')
@login_required  
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# --- ROUTE 5: Register ---
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        student_id = request.form.get('studentId', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirmPassword', '')
    
        errors = []
        
        # Basic validation
        if not all([first_name, last_name, student_id, email, password, confirm_password]):
            errors.append('All fields are required.')  
        
        if password != confirm_password:
            errors.append('Passwords do not match.')
            
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        try:
            full_name = f"{first_name} {last_name}"
            new_user = User(
                username=email,
                name=full_name,
                role='Student',
                std_id=student_id,
                register_date=datetime.utcnow().date()
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            db.session.rollback()
            # Check for duplicate key error (usually means user exists)
            flash('An error occurred. This email or Student ID might already be registered.', 'danger')
            print(f"Error: {e}")
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

# --- ROUTE 6: About Us ---
@main_bp.route('/about-us')
def about_us():
    return render_template('aboutus.html', user=current_user)