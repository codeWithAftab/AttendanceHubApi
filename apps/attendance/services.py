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


# standard imports
from django.db import transaction, IntegrityError
from apps.accounts.services import create_user
from apps.accounts.decorators import manager_role_required, staff_member_role_required
from django.utils.timezone import now
import pytz

# local imports
from .models import StaffManager, StaffMember, CustomUser
from .models import Shift, Attendance
from helper.validation import validate_weekly_off_list
from typing import Dict
from schema.request import ShiftSchema, VALID_DAYS
from exceptions.restapi import CustomAPIException
from .queries import *
from .validations import validate_attendance_request, validate_shift_interchange_request


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


def _create_shift_interchange_request(*, 
                                      requester: StaffMember,
                                      target: StaffMember,
                                      requester_shift: Shift,
                                      target_shift: Shift ):
    if is_any_pending_interchange_request_exist(target=target, 
                                                requester=requester,
                                                target_shift=target_shift, 
                                                requester_shift=requester_shift):
        
        raise CustomAPIException(error_code="ShiftInterchangeRequestAlreadyPending")
    
    shift_request = ShiftInterchangeRequest.objects.create(
                requester=requester,
                target=target,
                requester_shift=requester_shift,
                target_shift=target_shift
        )
    return shift_request


@staff_member_role_required
def request_shift_interchange(*,
                              staff_user: CustomUser,
                              target_email: str,
                              requester_shift_id: int,
                              target_shift_id: int,
                              **kwargs
                              ):
    """
    Handles a request for shift interchange between staff members.

    Args:
        staff_user (CustomUser): The staff user making the request.
        target_email (str): The email of the staff member whose shift is being targeted.
        requester_shift_id (int): The ID of the shift the requester wants to interchange.
        target_shift_id (int): The ID of the shift the target staff member currently has.

    Raises:
        CustomAPIException: If validation or processing fails.
    """

    targeted_staff_member = get_staff_member_by_email(email=target_email)
    requester_staff_member = get_staff_member_by_email(email=staff_user.email)

    # Validate the shift interchange request
    requester_shift, target_shift = validate_shift_interchange_request(
        requester_staff_member=requester_staff_member,
        requester_shift_id=requester_shift_id,
        targeted_staff_member=targeted_staff_member,
        target_shift_id=target_shift_id
    )

    return _create_shift_interchange_request(requester=requester_staff_member, 
                                             target=targeted_staff_member, 
                                             requester_shift=requester_shift,
                                             target_shift=target_shift )
    

@staff_member_role_required
def get_shift_interchange_requests(*,
                                  staff_user: CustomUser ):
    staff_member = get_staff_member_by_email(email=staff_user.email)
    return ShiftInterchangeRequest.objects.filter(target=staff_member, status="pending")


def __interchange_shift(interchange_request):
    """
    Interchange shifts between two staff members as per the interchange request.

    Args:
        interchange_request (ShiftInterchangeRequest): The interchange request object containing the shifts to be interchanged.
    """
    requester_shift = interchange_request.requester_shift
    target_shift = interchange_request.target_shift

    # Swap the staff members assigned to the shifts
    requester_shift.shift_start, target_shift.shift_start = target_shift.shift_start, requester_shift.shift_start
    requester_shift.shift_end, target_shift.shift_end = target_shift.shift_end, requester_shift.shift_end

    # Mark the interchange request as approved
    interchange_request.status = 'approved'

    # Save the updated shifts and interchange request
    try:
        with transaction.atomic():
            requester_shift.save()
            target_shift.save()
            interchange_request.save()

            print("Shifts successfully interchanged.")
        return interchange_request
    
    except IntegrityError as e:
        print("Error during shift interchange:", str(e))
        # Handle exception (e.g., rollback, log error)
        raise CustomAPIException(detail=f"Error :- {e}")


def _approve_or_reject_shift_interchange_request(interchange_request: ShiftInterchangeRequest, status: str):
    if status == "rejected":
        interchange_request.status = "rejected"
        interchange_request.save()
        return interchange_request
    
    
    return __interchange_shift(interchange_request=interchange_request)

@staff_member_role_required
def update_shift_interchange_request_status(*, 
                                     staff_user: CustomUser,
                                     request_id: int,
                                     status: str,
                                     **kwargs ):
    staff_member = get_staff_member_by_email(email=staff_user.email)
    interchange_request = get_shift_interchange_request_by_id(staff_member=staff_member, 
                                                              request_id=request_id )
    
    if not interchange_request:
        raise CustomAPIException(error_code="InterchangeRequestNotFound")
    
    return _approve_or_reject_shift_interchange_request(interchange_request=interchange_request, status=status)
    


