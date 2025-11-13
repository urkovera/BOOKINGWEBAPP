from app.models import Reserve, Room
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

def check_room_availability(room_id, start_time, end_time, exclude_reserve_id=None):
    """
    Check if a room is available for the given time slot
    Returns True if available, False otherwise
    """
    query = Reserve.query.filter(
        Reserve.room_id == room_id,
        Reserve.status.in_(['Pending', 'Approved']),
        or_(
            and_(Reserve.start_time <= start_time, Reserve.end_time > start_time),
            and_(Reserve.start_time < end_time, Reserve.end_time >= end_time),
            and_(Reserve.start_time >= start_time, Reserve.end_time <= end_time)
        )
    )
    
    if exclude_reserve_id:
        query = query.filter(Reserve.reserve_id != exclude_reserve_id)
    
    return query.count() == 0

def get_conflicting_reservations(room_id, start_time, end_time, exclude_reserve_id=None):
    """
    Get all reservations that conflict with the given time slot
    """
    query = Reserve.query.filter(
        Reserve.room_id == room_id,
        Reserve.status == 'Pending',
        or_(
            and_(Reserve.start_time <= start_time, Reserve.end_time > start_time),
            and_(Reserve.start_time < end_time, Reserve.end_time >= end_time),
            and_(Reserve.start_time >= start_time, Reserve.end_time <= end_time)
        )
    )
    
    if exclude_reserve_id:
        query = query.filter(Reserve.reserve_id != exclude_reserve_id)
    
    return query.all()

def cascade_decline_conflicts(approved_reservation):
    """
    Automatically decline all conflicting pending reservations
    when a reservation is approved
    """
    conflicts = get_conflicting_reservations(
        approved_reservation.room_id,
        approved_reservation.start_time,
        approved_reservation.end_time,
        approved_reservation.reserve_id
    )
    
    for conflict in conflicts:
        conflict.status = 'Declined'
        conflict.approve_by = approved_reservation.approve_by
        conflict.approve_date = datetime.utcnow().date()
    
    return len(conflicts)

def get_room_statistics(room_id, date):
    """
    Get booking statistics for a room on a specific date
    Returns dict with pending_count and approved_count
    """
    pending = Reserve.query.filter(
        Reserve.room_id == room_id,
        Reserve.book_date == date,
        Reserve.status == 'Pending'
    ).count()
    
    approved = Reserve.query.filter(
        Reserve.room_id == room_id,
        Reserve.book_date == date,
        Reserve.status == 'Approved'
    ).count()
    
    return {
        'pending_count': pending,
        'approved_count': approved,
        'total_requests': pending + approved
    }

def mark_completed_bookings():
    """
    Mark past bookings as completed
    Should be run periodically (e.g., daily cron job)
    """
    now = datetime.utcnow()
    
    expired = Reserve.query.filter(
        Reserve.status == 'Approved',
        Reserve.end_time < now
    ).update({'status': 'Expired'})
    
    return expired

def validate_booking_time(start_time, end_time):
    """
    Validate booking time constraints
    Returns (is_valid, error_message)
    """
    if start_time >= end_time:
        return False, "End time must be after start time"
    
    if start_time < datetime.utcnow():
        return False, "Cannot book in the past"
    
    duration = (end_time - start_time).total_seconds() / 3600
    if duration > 4:
        return False, "Booking duration cannot exceed 4 hours"
    
    if duration < 0.5:
        return False, "Booking duration must be at least 30 minutes"
    
    return True, None

def format_status_color(status):
    """
    Get color code for status
    """
    colors = {
        'Pending': 'yellow',
        'Approved': 'green',
        'Declined': 'red',
        'Expired': 'grey'
    }
    return colors.get(status, 'grey')