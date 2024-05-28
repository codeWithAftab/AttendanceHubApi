from .models import *
from apps.accounts.models import CustomUser
from exceptions.restapi import CustomAPIException
from apps.accounts.services import get_user_by_user_id

def _is_owner_has_fitness_centre(user:CustomUser) -> bool:
    try:
       fitness_centre = user.fitness_centre 
    except Exception as e:
        fitness_centre = None
    
    if fitness_centre:
        return True
    
    return False


def _get_fitness_centre_by_owner(owner: CustomUser) -> FitnessCentre:
    try:
        return owner.fitness_centre 
    
    except Exception as e:
        raise CustomAPIException(detail="You dont have access.")
        
    
def register_fitness_centre(*,
                          owner: CustomUser,
                          name: str,
                          **validated_data
                          ):
    if not owner.is_partner:
        raise CustomAPIException(detail="You dont have access to create fitness centre.")
    
    if _is_owner_has_fitness_centre(owner):
        raise CustomAPIException(error_code="UserAlreadyHasFitnessCentre")
    
    
    return FitnessCentre.objects.create(owner=owner,
                                        name=name,
                                        **validated_data
                                        )

def get_fitness_centre_by_owner(owner: CustomUser):
    if not owner.is_partner:
        raise CustomAPIException(detail="You dont have access to create fitness centre.")
    
    try:
        fitness_centre = FitnessCentre.objects.get(owner=owner)
        return fitness_centre
    
    except:
        raise CustomAPIException(detail=str(e))
    
def create_membership_plan(*, 
                           owner: CustomUser, 
                           **validated_data ):
    
    fitness_centre = _get_fitness_centre_by_owner(owner)

    membership = FitnessCentreMembership.objects.create(fitness_centre=fitness_centre, 
                                                        **validated_data )
    
    return membership

def delete_membership_plan(*, 
                           owner: CustomUser, 
                           membership_id: int, **kwargs ):
    
    fitness_centre = _get_fitness_centre_by_owner(owner)

    try:
        membership = FitnessCentreMembership.objects.get( fitness_centre=fitness_centre, 
                                                            id=membership_id )
        
        membership.delete()
    
    except:
        raise CustomAPIException(detail="Membership Already deleted ")

def update_membership_plan(*, 
                           owner: CustomUser, 
                           membership_id: int, **update_fields ):
    
    fitness_centre = _get_fitness_centre_by_owner(owner)
    try:
        membership = FitnessCentreMembership.objects.get( fitness_centre=fitness_centre, 
                                                            id=membership_id )
        
        for field , value in update_fields.items():
            print(field, value)
            setattr(membership, field, value)

        membership.save()
        return membership
    
    except:
        raise CustomAPIException(detail="Membership not Found ")


def add_user_to_fitness_centre(*, 
                               owner: CustomUser, 
                               user_id: str ) -> FitnessCentre:
    fitness_centre = _get_fitness_centre_by_owner(owner=owner)
    member = get_user_by_user_id(user_id=user_id)
    fitness_centre.joined_members.add(member)
    return fitness_centre

def remove_user_from_fitness_centre(*, 
                               owner: CustomUser, 
                               user_id: str ) -> FitnessCentre:
    fitness_centre = _get_fitness_centre_by_owner(owner=owner)
    member = get_user_by_user_id(user_id=user_id)
    fitness_centre.joined_members.remove(member)
    return fitness_centre
