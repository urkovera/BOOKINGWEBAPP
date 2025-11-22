from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(100), primary_key=True)  # CHANGED!
    name = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum('Student', 'Professor', name='user_role'), nullable=False)
    hash_password = db.Column(db.Text, nullable=False)
    std_id = db.Column(db.String(11), nullable=True)
    register_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    
    # Relationships
    reservations = db.relationship('Reserve', foreign_keys='Reserve.reserve_by', backref='reserver')
    approvals = db.relationship('Reserve', foreign_keys='Reserve.approve_by', backref='approver')
    
    def get_id(self):
        """
        Override get_id to return username (email)
        Flask-Login uses this to get the user ID for the session
        """
        return self.username
    
    def set_password(self, password):
        """Hash password before storing"""
        self.hash_password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.hash_password, password)
    
    @property
    def is_professor(self):
        """Check if user is a professor"""
        return self.role == 'Professor'
    
    @property
    def is_student(self):
        """Check if user is a student"""
        return self.role == 'Student'
class Room(db.Model):
    __tablename__ = 'rooms'
    
    room_id = db.Column(db.String(7), primary_key=True)
    chair = db.Column(db.Integer, nullable=False)
    projector = db.Column(db.Boolean, nullable=False)
    air_conditioner = db.Column(db.Integer, nullable=False)
    computer = db.Column(db.Boolean, nullable=False)
    
    # Relationships
    reservations = db.relationship('Reserve', backref='room')

class Reserve(db.Model):
    __tablename__ = 'reserves'
    
    reserve_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.String(7), db.ForeignKey('rooms.room_id'), nullable=False)
    book_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('Pending', 'Approved', 'Declined', 'Expired', name='reserve_status'), 
                       nullable=False, default='Pending')
    approve_by = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=True)
    approve_date = db.Column(db.Date, nullable=True)
    reserve_by = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
    reserve_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.Text, nullable=True)