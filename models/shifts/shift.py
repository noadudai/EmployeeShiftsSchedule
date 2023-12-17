import datetime
from uuid import uuid4

from .shifts_types_enum import ShiftTypesEnum


class Shift:

    def __init__(self, shift_type: ShiftTypesEnum, start_time: datetime.datetime, end_time: datetime.datetime):
        # Generates a random UUID
        self.shift_id = uuid4()
        self.shift_type = shift_type
        self.start_time = start_time
        self.end_time = end_time
