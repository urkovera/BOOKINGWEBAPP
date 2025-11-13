from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Room, Reserve
from app.utils import check_room_availability, validate_booking_time
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_booking():
    if request.method == 'POST':
        # Handle booking creation
        pass
    
    rooms = Room.query.all()
    return render_template('booking/new_booking.html', rooms=rooms)

@booking_bp.route('/rooms/<date>')
@login_required
def view_rooms(date):
    # Display available rooms for a specific date
    pass