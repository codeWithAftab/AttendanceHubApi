from apps.core.models import CustomErrors

error_messages = [
    {"code": "InterchangeRequestNotFound", "message": "Interchange request not found", "status": 400},
    {"code": "SameDayMustInInterchange", "message": "Same day is must", "status": 400},
    {"code": "ShiftInterchangeRequestAlreadyPending", "message": "Same Shift Interchange Request Already Pending", "status": 400},
    {"code": "TargetedShiftNotFound", "message": "Targeted Shift not found", "status": 400},
    {"code": "RequesterShiftNotFound", "message": "Requester shift not found error", "status": 400},
    {"code": "StaffUserNotFound", "message": "Staff User not found with provided email", "status": 400},
    {"code": "AttendanceAlreadyMarked", "message": "User already marked their attendance", "status": 400},
    {"code": "OutOfAttendanceWindow", "message": "Attendance can only be marked within 1 hour of your shift end time", "status": 400},
    {"code": "CannotAssignWeekOffShift", "message": "Manager can only assign shift on weekdays not for weekends", "status": 400},
    {"code": "WeeklyOffToday", "message": "Weekly off today", "status": 400},
    {"code": "NoShiftForToday", "message": "No shift for today", "status": 400},
    {"code": "OutOfShiftHours", "message": "Out of shift hours", "status": 400},
    {"code": "WrongEmployeeId", "message": "Employee ID is not correct, please check", "status": 400},
    {"code": "PermissionError", "message": "User does not have required permissions to perform this task", "status": 401},
    {"code": "MissingFieldError", "message": "These required fields must be present", "status": 400},
    {"code": "EmailAlreadyExist", "message": "This email already exists in the database", "status": 403}
]


def create_errors():
    custom_error_objs = []
    
    for error_message in error_messages:
        err = CustomErrors(code=error_message["code"], status_code=error_message["status"], detail=error_message["message"])
        custom_error_objs.append(err)

    try:
        CustomErrors.objects.bulk_create(custom_error_objs)
        print("creation done.")
    except Exception as e:
        print(f"Custom Errors already created.. {e}")
