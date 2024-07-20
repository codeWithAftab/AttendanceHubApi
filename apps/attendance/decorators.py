from exceptions.restapi import CustomAPIException

def manager_role_required(fx):
    def mfx(*args, **kwargs):
        user = kwargs.get("manager")
        print(user.role)
        if user.role != 0:
            raise CustomAPIException(detail="PermissionError", error_code="PermissionError")
        
        return fx(*args, **kwargs)
    
    return mfx