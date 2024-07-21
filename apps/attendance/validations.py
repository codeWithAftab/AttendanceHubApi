"""
validations.py

This module contains validation functions for the attendance management system.
These functions are used to ensure that requests meet certain criteria before they are processed.

Functions:

- validate_attendance_request(staff_member: StaffMember, current_day: str, current_time: time):
    Validates whether a staff member can mark attendance based on their shift and weekly off.
"""
import pytz
from exceptions.restapi import CustomAPIException
from .models import StaffMember
from django.utils.timezone import now, make_aware
from datetime import datetime, timedelta
from django.conf import settings  # Import settings
from .queries import *

def validate_attendance_request(staff_member: StaffMember, current_day: str, current_datetime):
    """
    Validates whether a staff member can mark attendance.

    Args:
        staff_member (StaffMember): The staff member attempting to mark attendance.
        current_day (str): The current day of the week.
        current_time (time): The current time.

    Raises:
        CustomAPIException: If today is a weekly off day, no shift is found for today, 
                            or the current time is outside of shift hours.
    """
    # Check if today is a weekly off day
    if current_day in staff_member.weekly_off:
        raise CustomAPIException(
            detail=f"Today is {current_day} and this is your weekly off, so you cannot mark attendance.", 
            error_code="WeeklyOffToday"
        )

    shift = get_staff_member_shift(staff_member=staff_member, day=current_day)
    if not shift:
        raise CustomAPIException(
            detail="No shift found for today.",
            error_code="NoShiftForToday"
        )

    # Check if current time is within the shift hours
    print("start_time", shift.shift_start)
    print("current_time", current_datetime.time())
    print("end_time", shift.shift_end)

    if not (shift.shift_start <= current_datetime.time() <= shift.shift_end):
        raise CustomAPIException(
            detail="You can only mark attendance within shift hours.",
            error_code="OutOfShiftHours"
        )

    # Combine the shift start time with today's date
    shift_start_datetime = datetime.combine(now().date(), shift.shift_start)
    shift_end_datetime = datetime.combine(now().date(), shift.shift_end)
    

    # Make the shift datetimes timezone-aware
    tz = pytz.timezone(settings.TIME_ZONE)
    shift_start_datetime = make_aware(shift_start_datetime, timezone=tz)
    shift_end_datetime = make_aware(shift_end_datetime, timezone=tz)
  
    # Calculate the time range for marking attendance
    one_hour_after_shift_start = shift_start_datetime + timedelta(hours=1)
    print("one hour", (one_hour_after_shift_start > current_datetime <= shift_end_datetime))
    # Check if the current time is within 1 hour of the shift end time
    if not (one_hour_after_shift_start > current_datetime <= shift_end_datetime):
        raise CustomAPIException(
            detail="Attendance can only be marked within 1 hour of your shift end time.",
            error_code="OutOfAttendanceWindow"
        )
    

def validate_shift_interchange_request(*, 
                                       requester_staff_member: StaffMember, 
                                       requester_shift_id: int, 
                                       targeted_staff_member: StaffMember, 
                                       target_shift_id: int) -> None:
    """
    Validates the shift interchange request.

    Args:
        requester_staff_member (StaffMember): The staff member requesting the shift interchange.
        requester_shift_id (int): The ID of the requester's shift.
        targeted_staff_member (StaffMember): The staff member targeted for the shift interchange.
        target_shift_id (int): The ID of the target's shift.

    Raises:
        CustomAPIException: If validation fails for various reasons.
    """
    # Check if targeted staff member exists
    if not targeted_staff_member:
        raise CustomAPIException(detail="Targeted staff member not found.", error_code="StaffUserNotFound")
    
    # Fetch and validate requester's shift
    requester_shift = get_staff_member_shift_by_id(staff_member=requester_staff_member, shift_id=requester_shift_id)
    if not requester_shift:
        raise CustomAPIException(detail="Requester shift not found.", error_code="RequesterShiftNotFound")
    
    # Fetch and validate target's shift
    target_shift = get_staff_member_shift_by_id(staff_member=targeted_staff_member, shift_id=target_shift_id)
    if not target_shift:
        raise CustomAPIException(detail="Targeted shift not found.", error_code="TargetedShiftNotFound")
    
    if target_shift.day != requester_shift.day:
        raise CustomAPIException(detail="Day of both Shift must be Same.", error_code="SameDayMustInInterchange")

    return requester_shift, target_shift
