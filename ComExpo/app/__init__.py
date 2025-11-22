from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.booking import booking_bp
    from app.routes.approval import approval_bp
    from app.routes.history import history_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(approval_bp, url_prefix='/approval')
    app.register_blueprint(history_bp, url_prefix='/history')

    # --- START NEW CODE ---
    # This block ensures tables are created when the app starts
    with app.app_context():
        # Import your models here so SQLAlchemy knows about them before creating
        # Adjust 'from app.models' if your models are in a different file
        from app.models import User 
        # from app.models import Booking, Room (import other models if needed)
        
        db.create_all()
    # --- END NEW CODE ---
    
    return app