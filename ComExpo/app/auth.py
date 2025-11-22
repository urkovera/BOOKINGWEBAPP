from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def login_required_role(*roles):
    """
    Decorator to require specific roles for a route
    Usage: @login_required_role('Professor')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('main.login'))
            
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def is_professor():
    """Check if current user is a professor"""
    return current_user.is_authenticated and current_user.role == 'Professor'

def is_student():
    """Check if current user is a student"""
    return current_user.is_authenticated and current_user.role == 'Student'

def get_user_role():
    """Get current user's role"""
    if current_user.is_authenticated:
        return current_user.role
    return None