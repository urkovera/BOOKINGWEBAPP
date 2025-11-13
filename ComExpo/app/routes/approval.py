from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Reserve
from app.auth import login_required_role
from app.utils import cascade_decline_conflicts

approval_bp = Blueprint('approval', __name__)

@approval_bp.route('/pending')
@login_required_role('Professor')
def pending_requests():
    # Show pending requests with filters
    pass

@approval_bp.route('/approve/<int:reserve_id>', methods=['POST'])
@login_required_role('Professor')
def approve_request(reserve_id):
    # Approve booking and cascade decline conflicts
    pass

@approval_bp.route('/decline/<int:reserve_id>', methods=['POST'])
@login_required_role('Professor')
def decline_request(reserve_id):
    # Decline booking
    pass