from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Room, Reserve
# Added 'cascade_decline_conflicts' to imports
from app.utils import check_room_availability, validate_booking_time, cascade_decline_conflicts
from datetime import datetime

# --- Blueprint Definition ---
booking_bp = Blueprint('booking', __name__) 
# ----------------------------

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

            if not check_room_availability(room_id, start_dt, end_dt):
                flash('This room is already booked for the selected time.', 'danger')
                return render_template('booking/new_booking.html', rooms=rooms, room_images=room_images)

            # 5. Determine Status Based on Role
            # Default for Students
            initial_status = 'Pending'
            approver = None
            approve_date_val = None
            
            # Logic for Professors (Auto-Approve)
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
                # If auto-approved, cancel any conflicting pending requests
                declined_count = cascade_decline_conflicts(new_reservation)
                db.session.commit()
                flash(f'Booking confirmed successfully! (Auto-approved as Professor)', 'success')
            else:
                flash('Booking request submitted successfully! Waiting for approval.', 'success')

            return redirect(url_for('history.my_bookings'))

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