from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Reserve
from app.auth import login_required_role
from app.utils import cascade_decline_conflicts
from datetime import datetime

approval_bp = Blueprint('approval', __name__)

@approval_bp.route('/pending')
@login_required_role('Professor')
def pending_requests():
    # Fetch ALL bookings that are still pending
    pending_bookings = Reserve.query.filter_by(status='Pending').order_by(Reserve.reserve_id.desc()).all()
    
    return render_template('approval/request.html', bookings=pending_bookings)

@approval_bp.route('/approve/<int:reserve_id>', methods=['POST'])
@login_required_role('Professor')
def approve_request(reserve_id):
    reservation = Reserve.query.get_or_404(reserve_id)
    
    # 1. Update Status
    reservation.status = 'Approved'
    reservation.approve_by = current_user.username
    reservation.approve_date = datetime.utcnow().date()
       
    # 2. Automatically decline other students who wanted the same room/time
    declined_count = cascade_decline_conflicts(reservation)
     
    db.session.commit()
    
    flash(f'Request Approved! {declined_count} conflicting requests were automatically declined.', 'success')
    return redirect(url_for('approval.pending_requests'))

@approval_bp.route('/decline/<int:reserve_id>', methods=['POST'])
@login_required_role('Professor')
def decline_request(reserve_id):
    reservation = Reserve.query.get_or_404(reserve_id)
    
    # 1. Update Status
    reservation.status = 'Declined'
    reservation.approve_by = current_user.username
    reservation.approve_date = datetime.utcnow().date()
    
    db.session.commit()
    
    flash('Request Declined.', 'warning')
    return redirect(url_for('approval.pending_requests'))