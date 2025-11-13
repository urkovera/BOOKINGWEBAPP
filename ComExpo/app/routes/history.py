from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Reserve

history_bp = Blueprint('history', __name__)

@history_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Reserve.query.filter_by(reserve_by=current_user.username).all()
    return render_template('history/history.html', bookings=bookings)