from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Room, Reserve
from app.utils import validate_booking_time, cascade_decline_conflicts
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_booking():
    rooms = Room.query.all()
    
    # Image mapping
    room_images = {
        '1116': '1116room.jpg', 
        '1115': '1115room.jpg',
        '1121': '1121room.jpg',
        '1114': '1114room.jpg', 
        '1113': '1113room.jpg',
        '1112': '1112room.jpg'
    }

    if request.method == 'POST':
        # 1. Get Data from Form
        room_id = request.form.get('room_id')
        date_str = request.form.get('date')
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
        reason = request.form.get('reason')

        # 2. Basic Validation
        if not all([room_id, date_str, start_time_str, end_time_str, reason]):
            flash('Please fill in all fields.', 'danger')
            return render_template('booking/new_booking.html', rooms=rooms, room_images=room_images)

        try:
            # 3. Convert Strings to Python Objects
            start_dt = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M")
            book_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # 4. Logic Validation
            is_valid_time, error_msg = validate_booking_time(start_dt, end_dt)
            if not is_valid_time:
                flash(error_msg, 'danger')
                return render_template('booking/new_booking.html', rooms=rooms, room_images=room_images)

            # --- LOGIC TO ALLOW MULTIPLE PENDING REQUESTS ---
            
            # Check for conflicting APPROVED bookings
            conflicting_approved = Reserve.query.filter(
                Reserve.room_id == room_id,
                Reserve.status == 'Approved',
                Reserve.start_time < end_dt,
                Reserve.end_time > start_dt
            ).first()

            if conflicting_approved:
                flash(f'Room {room_id} is already APPROVED for another class at this time.', 'danger')
                return render_template('booking/new_booking.html', rooms=rooms, room_images=room_images)

            # Check for existing PENDING requests (for information only)
            pending_count = Reserve.query.filter(
                Reserve.room_id == room_id,
                Reserve.status == 'Pending',
                Reserve.start_time < end_dt,
                Reserve.end_time > start_dt
            ).count()

            # 5. Determine Status
            initial_status = 'Pending'
            approver = None
            approve_date_val = None
            
            # Auto-Approve for Professors
            if current_user.role == 'Professor':
                initial_status = 'Approved'
                approver = current_user.username
                approve_date_val = datetime.utcnow().date()

            # 6. Save to Database
            new_reservation = Reserve(
                room_id=room_id,
                book_date=book_date,
                start_time=start_dt,
                end_time=end_dt,
                reason=reason,
                reserve_by=current_user.username,
                status=initial_status,
                approve_by=approver,
                approve_date=approve_date_val
            )

            db.session.add(new_reservation)
            db.session.commit()
            
            # 7. Post-Booking Actions
            if initial_status == 'Approved':
                declined_count = cascade_decline_conflicts(new_reservation)
                db.session.commit()
                flash(f'Booking confirmed! (Auto-approved). {declined_count} other requests were declined.', 'success')
            else:
                if pending_count > 0:
                    flash(f'Request submitted! Note: There are {pending_count} other pending requests for this slot.', 'warning')
                else:
                    flash('Booking request submitted successfully! Waiting for approval.', 'success')

            # FIX: Redirect back to the booking page instead of history
            return redirect(url_for('booking.new_booking'))

        except ValueError:
            flash('Invalid date or time format.', 'danger')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash('An error occurred while processing your request.', 'danger')

    return render_template('booking/new_booking.html', rooms=rooms, room_images=room_images)

@booking_bp.route('/rooms/<date>')
@login_required
def view_rooms(date):
    pass 