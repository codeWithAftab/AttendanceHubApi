"""
queries.py

This module contains query functions used throughout the attendance management system.
Each function is designed to encapsulate common database queries, providing a
centralized and reusable way to interact with the database. 

Functions:

- get_staff_member_by_id(employee_id: str) -> Optional[StaffMember]:
    Retrieves a staff member by their employee ID.
    
- get_staff_member_shift(staff_member: CustomUser, day: str) -> Optional[Shift]:
    Retrieve the shift details for a specific staff member on a given day.
    
- get_staff_member_by_user(user: CustomUser) -> Optional[StaffMember]:
    Retrieve the staff member associated with a given user.
    
- get_staff_member_shifts(staff_member: StaffMember):
    Retrieve all shifts assigned to a staff member.
    
- is_member_already_marked_attendance(staff_member: StaffMember) -> bool:
    Check if a staff member has already marked attendance for the current day.
"""


from .models import *
from typing import Optional, Literal
from django.utils.timezone import now



def get_staff_member_by_id(employee_id: str) -> Optional[StaffMember]:
    """
    Retrieves a staff member by their employee ID.

    Args:
        employee_id (str): The ID of the employee to retrieve.

    Returns:
        Optional[StaffMember]: The staff member if found, otherwise None.
    """
    try:
        staff = StaffMember.objects.get(employee_id=employee_id)
        return staff
    except StaffMember.DoesNotExist:
        return None
    
def get_staff_member_shift_by_id(staff_member: StaffMember, shift_id: int):
    try:
        shift = Shift.objects.get(staff_member=staff_member, id=shift_id)
        return shift
    
    except Shift.DoesNotExist as e:
        print("Erro", e)
        return None
    
def is_any_pending_interchange_request_exist(target: StaffMember, 
                                             requester: StaffMember, 
                                             requester_shift: Shift,
                                             target_shift: Shift,
                                             **kwargs) -> bool:
    """
    Check if there are any pending shift interchange requests between the given target and requester for the specified shifts.

    Args:
        target (StaffMember): The staff member who is the target of the interchange request.
        requester (StaffMember): The staff member who is requesting the interchange.
        requester_shift (Shift): The shift requested by the requester to be interchanged.
        target_shift (Shift): The shift of the target to be interchanged.

    Returns:
        bool: True if there are any pending requests, False otherwise.
    """
    return ShiftInterchangeRequest.objects.filter(
        target=target, 
        requester=requester, 
        requester_shift=requester_shift,
        target_shift=target_shift, 
        status='pending'
    ).exists()


def get_staff_member_shift(staff_member: CustomUser, day: str) -> Optional[Shift]:
    """
    Retrieve the shift details for a specific staff member on a given day.

    Args:
        staff_member (CustomUser): The staff member for whom to get the shift.
        day (str): The day of the week to retrieve the shift for.

    Returns:
        Optional[Shift]: The shift object if found, otherwise None.
    """
    try:
        shift = Shift.objects.get(staff_member=staff_member, day=day)
        return shift
    
    except Shift.DoesNotExist:
        return None
    
def get_staff_member_by_user(user: CustomUser) -> Optional[StaffMember]:
    """
    Retrieve the staff member associated with a given user.

    Args:
        user (CustomUser): The user whose staff member record is to be retrieved.

    Returns:
        Optional[StaffMember]: The associated staff member or None if not found.
    """
    try:
        return StaffMember.objects.get(user=user)
    except StaffMember.DoesNotExist:
        return None

def get_staff_member_by_email(email: str) -> Optional[StaffMember]:
  
    try:
        return StaffMember.objects.get(user__email=email)
    except StaffMember.DoesNotExist:
        return None

def get_staff_member_shifts(staff_member: StaffMember):
    """
    Retrieve all shifts assigned to a staff member.

    Args:
        staff_member (StaffMember): The staff member whose shifts are to be retrieved.

    Returns:
        QuerySet: A queryset of Shift objects.
    """
    return Shift.objects.filter(staff_member=staff_member)

def is_member_already_marked_attendance(staff_member: StaffMember) -> bool:
    """
    Check if a staff member has already marked attendance for the current day.

    Args:
        staff_member (StaffMember): The staff member to check.

    Returns:
        bool: True if attendance has already been marked, False otherwise.
    """
    return Attendance.objects.filter(staff_member=staff_member, date=now().date()).exists()


def get_shift_interchange_request_by_id(*,
                                        staff_member: StaffMember = None,
                                        request_id: int):
    """
    Retrieves a shift interchange request by its ID, with optional staff member validation.

    Args:
        staff_member (StaffMember, optional): The staff member associated with the request. Defaults to None.
        request_id (int): The ID of the shift interchange request to retrieve.

    Returns:
        ShiftInterchangeRequest or None: The shift interchange request if found, otherwise None.
    """
    try:
   
        request = ShiftInterchangeRequest.objects.get(id=request_id, target=staff_member)

        return request
    except ShiftInterchangeRequest.DoesNotExist:
        return None
