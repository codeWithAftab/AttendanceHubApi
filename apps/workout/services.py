from .models import *

def get_all_body_parts(body_part_type: str ):
    return BodyPart.objects.filter(body_part_type=body_part_type)

def get_body_part_excercises(body_part_id: int, **kwargs):
    return Exercise.objects.filter(body_parts__id=body_part_id)