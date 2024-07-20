from .models import StaffManager, StaffMember, CustomUser
from apps.accounts.services import create_user
from apps.accounts.decorators import manager_role_required, staff_member_role_required
from django.utils.timezone import now

# local imports
from .models import Shift, Attendance
from helper.validation import validate_weekly_off_list
from typing import Dict
from schema.request import ShiftSchema, VALID_DAYS
from exceptions.restapi import CustomAPIException
from .queries import *


# internal use methods
def _create_staff_member_shift(*, 
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
                       shift: ShiftSchema ) -> Shift:
    
    staff_member = get_staff_member_by_id(employee_id=employee_id)

    if not staff_member:
        raise CustomAPIException(error_code="WrongEmployeeId")
    
    created_shift =  _create_staff_member_shift(staff_member=staff_member, shift=shift)
    return created_shift


@manager_role_required
def assign_staff_weekly_off(*, 
                            manager: CustomUser,
                            employee_id: str, 
                            weekly_off: VALID_DAYS ) -> StaffMember:
    staff_member = get_staff_member_by_id(employee_id=employee_id)
    if not staff_member:
        raise CustomAPIException(error_code="WrongEmployeeId")
    
    staff_member.weekly_off = weekly_off
    staff_member.save()

    return staff_member
    

# staff methods
@staff_member_role_required
def get_staff_assigned_shifts(*, 
                             staff_user: CustomUser
                             ):
    staff_member = get_staff_member_by_user(user=staff_user)
    if not staff_member:
        raise CustomAPIException(error_code="UserMustBeStaffMember")
    
    return get_staff_member_shifts(staff_member=staff_member)


def _mark_staff_attendance(staff_member: StaffMember, image):
    current_day = now().strftime('%A').lower()
    current_time= now().time()
    print("current_day", current_day)

    # Check if today is a weekly off day
    if current_day in staff_member.weekly_off:
        raise CustomAPIException(
            detail=f" Today is {current_day} and this is your weekly off so you can not mark attendance.", 
            error_code="WeeklyOffToday"
            )

    
    shift = get_staff_member_shift(staff_member=staff_member, day=current_day)
    if not shift:
        raise CustomAPIException(
                detail="No shift found for today.",
                error_code="NoShiftForToday"
            )

     # Check if current time is within the shift hours
    if not (shift.shift_start <= current_time <= shift.shift_end):
        raise CustomAPIException(
            detail="You can only mark attendance within shift hours.",
            error_code="OutOfShiftHours"
        )
    
    try:
        attendance = Attendance.objects.create(
                staff_member=staff_member,
                date=now().date(),
                timestamp=now(),
                image=image
            )
    except:
        pass
    
    return attendance
    



@staff_member_role_required
def mark_attendance(*, 
                    staff_user: CustomUser,
                    image,
                    **kwargs
                    ):
    staff_member = get_staff_member_by_user(user=staff_user)

    if not staff_member:
        raise CustomAPIException(error_code="UserMustBeStaffMember")
    
    return _mark_staff_attendance(staff_member=staff_member, image=image)