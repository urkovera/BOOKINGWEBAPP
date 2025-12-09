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
    
    @app.template_filter('dateformat')
    def dateformat(value, format='%d %B %Y'):
        if value is None:
            return ""
        return value.strftime(format)
    
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
    def seed_database():
        from app.models import Room

        # DATA ENTRY: TYPE YOUR DATA HERE
        rooms_to_seed = [
            Room(room_id='CPE-1116', chair=42, projector=True, air_conditioner=2, computer=False),
            Room(room_id='CPE-1115', chair=81 projector=True, air_conditioner=4, computer=False),
            Room(room_id='CPE-1121', chair=84, projector=True, air_conditioner=4, computer=False),
            Room(room_id='CPE-1114', chair=57, projector=True, air_conditioner=4, computer=False),
            Room(room_id='CPE-1113', chair=51, projector=True, air_conditioner=4, computer=True),
            Room(room_id='CPE-1112', chair=52, projector=True, air_conditioner=4, computer=True),
            # Add as many as you want...
        ]
        added_count = 0
        
        # 2. Loop through each room and check individually
        for room_data in rooms_to_seed:
            existing_room = Room.query.get(room_data.room_id)
            
            if not existing_room:
                # It doesn't exist yet, so add it
                db.session.add(room_data)
                added_count += 1
        
        # 3. Commit only if we actually added something
        if added_count > 0:
            try:
                db.session.commit()
                print(f"✅ added {added_count} new rooms to the database!")
            except Exception as e:
                db.session.rollback()
                print(f"Error seeding database: {e}")
        else:
            print("Database is already up to date.")

    return app
