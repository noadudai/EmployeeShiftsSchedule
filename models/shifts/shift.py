import datetime
from uuid import uuid4

from .shifts_types_enum import ShiftTypesEnum


class Shift:

    def __init__(self, shift_type: ShiftTypesEnum, start_of_shift: datetime.datetime, end_of_shift: datetime.datetime):
        # Generates a random UUID
        self.shift_id = uuid4()
        self.shift_type = shift_type
        self.start_of_shift = start_of_shift
        self.end_of_shift = end_of_shift
