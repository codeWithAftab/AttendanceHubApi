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