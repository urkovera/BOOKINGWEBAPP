from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.booking import booking_bp
    from app.routes.approval import approval_bp
    from app.routes.history import history_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(booking_bp, url_prefix='/booking')
    app.register_blueprint(approval_bp, url_prefix='/approval')
    app.register_blueprint(history_bp, url_prefix='/history')
    
    return app