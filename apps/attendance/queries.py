from .models import *
from typing import Optional, Literal


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
    

def get_staff_member_by_user(user: CustomUser):
    try:
        staff_member = StaffMember.objects.get(user=user)
        return staff_member
    
    except StaffMember.DoesNotExist:
        return None
  

def get_staff_member_shifts(staff_member: StaffMember):
    shifts = Shift.objects.filter(staff_member=staff_member)
    return shifts