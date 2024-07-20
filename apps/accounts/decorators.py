# local modules.
from exceptions.restapi import CustomAPIException

def manager_role_required(fx):
    def mfx(*args, **kwargs):
        user = kwargs.get("manager")
        print(user.role)
        if user.role != "manager":
            raise CustomAPIException(detail="User role should be the 'manager' to perform this action.",  error_code="PermissionError")
        
        return fx(*args, **kwargs)
    
    return mfx

def staff_member_role_required(fx):
    def mfx(*args, **kwargs):
        user = kwargs.get("staff_user")
        print(user.role)
        if user.role != "staff":
            raise CustomAPIException(detail="User role should be the 'staff member' to perform this action.",  error_code="PermissionError")
        
        return fx(*args, **kwargs)
    
    return mfx