from dataclasses import dataclass
from datetime import time
from typing import Literal, TypedDict


VALID_DAYS = Literal['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


class ShiftSchema(TypedDict):
    day: Literal['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    shift_start: time
    shift_end: time


