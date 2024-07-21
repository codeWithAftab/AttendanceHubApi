"""
services.py

This module contains the business logic for the attendance management system. 
It includes functions for managing shifts, assigning weekly off days, and marking attendance for staff members.
Each function interacts with the database through query functions defined in queries.py and ensures proper 
role-based access control through decorators.

Functions:

-   _create_or_update_staff_member_shift(*, staff_member: StaffMember, shift: Dict[str, any]) -> Shift:
    Create or update the shift for a specific staff member.

- assign_staff_shift(*, manager: CustomUser, employee_id: str, shift: ShiftSchema) -> Shift:
    Assign or update a shift for a staff member.
    
- assign_staff_weekly_off(*, manager: CustomUser, employee_id: str, weekly_off: VALID_DAYS) -> StaffMember:
    Assign a weekly off day for a staff member.
    
- get_staff_assigned_shifts(*, staff_user: CustomUser):
    Retrieve assigned shifts for a staff member.
    
- _mark_staff_attendance(staff_member: StaffMember, image) -> Attendance:
    Mark attendance for a staff member.
    
- mark_attendance(*, staff_user: CustomUser, image, **kwargs) -> Attendance:
    Mark attendance for a staff member.
"""



from .models import StaffManager, StaffMember, CustomUser
from apps.accounts.services import create_user
from apps.accounts.decorators import manager_role_required, staff_member_role_required
from django.utils.timezone import now
import pytz
# local imports
from .models import Shift, Attendance
from helper.validation import validate_weekly_off_list
from typing import Dict
from schema.request import ShiftSchema, VALID_DAYS
from exceptions.restapi import CustomAPIException
from .queries import *
from .validations import validate_attendance_request


# internal use methods
def _create_or_update_staff_member_shift(*, 
                               staff_member: StaffMember,  
                               shift: Dict[str, any]) -> Shift:
    """
    Create or update the shift for a specific staff member.

    Args:
        staff_member (StaffMember): The staff member for whom to create or update the shift.
        shift (Dict[str, any]): The shift details.

    Returns:
        Shift: The created or updated shift object.
    """
    # Fetch existing shift
    member_shift = get_staff_member_shift(staff_member=staff_member, day=shift.get("day"))

    if not member_shift:
        # Create a new shift if it doesn't exist
        new_shift = Shift.objects.create(
            staff_member=staff_member,
            **shift
        )
        return new_shift

    # Update existing shift with new details
    for key, value in shift.items():
        setattr(member_shift, key, value)
    
    member_shift.save()
    return member_shift


@manager_role_required
def assign_staff_shift(*, 
                       manager: CustomUser,
                       employee_id: str,
                       shift: ShiftSchema) -> Shift:
    """
    Assign or update a shift for a staff member.
    
    Args:
        manager (CustomUser): The manager performing the assignment.
        employee_id (str): The ID of the employee.
        shift (ShiftSchema): The shift details.

    Returns:
        Shift: The created or updated shift.
    """
    staff_member = get_staff_member_by_id(employee_id=employee_id)
    if not staff_member:
        raise CustomAPIException(error_code="WrongEmployeeId")
    
    if shift["day"] in staff_member.weekly_off:
        raise CustomAPIException(error_code="CannotAssignWeekOffShift")
    
    created_shift = _create_or_update_staff_member_shift(staff_member=staff_member, shift=shift)
    return created_shift

@manager_role_required
def assign_staff_weekly_off(*, 
                            manager: CustomUser,
                            employee_id: str, 
                            weekly_off: VALID_DAYS) -> StaffMember:
    """
    Assign a weekly off day for a staff member.
    
    Args:
        manager (CustomUser): The manager performing the assignment.
        employee_id (str): The ID of the employee.
        weekly_off (VALID_DAYS): The day to set as the weekly off.

    Returns:
        StaffMember: The updated staff member.
    """
    staff_member = get_staff_member_by_id(employee_id=employee_id)
    if not staff_member:
        raise CustomAPIException(error_code="WrongEmployeeId")
    
    staff_member.weekly_off = weekly_off
    staff_member.save()
    return staff_member

@staff_member_role_required
def get_staff_assigned_shifts(*, 
                             staff_user: CustomUser):
    """
    Retrieve assigned shifts for a staff member.
    
    Args:
        staff_user (CustomUser): The staff member making the request.

    Returns:
        List[Shift]: The list of assigned shifts.
    """
    staff_member = get_staff_member_by_user(user=staff_user)
    if not staff_member:
        raise CustomAPIException(error_code="UserMustBeStaffMember")
    
    return get_staff_member_shifts(staff_member=staff_member)

def _mark_staff_attendance(staff_member: StaffMember, image) -> Attendance:
    """
    Mark attendance for a staff member.
    
    Args:
        staff_member (StaffMember): The staff member marking attendance.
        image: The image used for attendance marking.

    Returns:
        Attendance: The created attendance record.
    """
    # Get current time in UTC
    current_utc_time = now()

    # Convert UTC time to IST
    ist = pytz.timezone('Asia/Kolkata')
    current_datetime = current_utc_time.astimezone(ist)

    current_day = current_datetime.strftime('%A').lower()
 
    validate_attendance_request(staff_member=staff_member, 
                                current_day=current_day, 
                                current_datetime=current_datetime )
    

    if is_member_already_marked_attendance(staff_member=staff_member):
        raise CustomAPIException(
            detail="User Already Marked thier attendance.",
            error_code="AttendanceAlreadyMarked"
        )
    
    attendance = Attendance.objects.create(
            staff_member=staff_member,
            date=now().date(),
            timestamp=now(),
            image=image
        )

    return attendance


@staff_member_role_required
def mark_attendance(*, 
                    staff_user: CustomUser,
                    image,
                    **kwargs) -> Attendance:
    """
    Mark attendance for a staff member.
    
    Args:
        staff_user (CustomUser): The staff member making the request.
        image: The image used for attendance marking.

    Returns:
        Attendance: The created attendance record.
    """
    staff_member = get_staff_member_by_user(user=staff_user)
    if not staff_member:
        raise CustomAPIException(error_code="UserMustBeStaffMember")
    
    return _mark_staff_attendance(staff_member=staff_member, image=image)
