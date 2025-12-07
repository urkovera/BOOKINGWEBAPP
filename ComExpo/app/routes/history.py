from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Reserve
from app import db
from datetime import datetime # <--- Import this

history_bp = Blueprint('history', __name__)

@history_bp.route('/my-bookings')
@login_required
def my_bookings():
    # 1. Fetch user's bookings
    bookings = Reserve.query.filter_by(reserve_by=current_user.username).all()
    
    # 2. AUTO-EXPIRE LOGIC
    # Get current time
    now = datetime.now() 
    data_changed = False

    for booking in bookings:
        # If booking is Pending AND the End Time has passed
        if booking.status == 'Pending' and booking.end_time < now:
            booking.status = 'Expired'
            data_changed = True
    
    # 3. Save changes to Database if any updates happened
    if data_changed:
        db.session.commit()

    # 4. Render the page (now with updated statuses)
    return render_template('history/history.html', bookings=bookings, user=current_user)