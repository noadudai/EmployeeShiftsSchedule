from .shift_type import ShiftType
from .shifts_types_enum import ShiftTypesEnum
import datetime


class Shift:

    def __init__(self, shift_type: ShiftType, start_date_of_shift: datetime.date, end_date_of_shift: datetime.date):
        self.shift_type = shift_type
        self.start_date_of_shift = start_date_of_shift
        self.end_date_of_shift = end_date_of_shift

    def get_str_start_date(self):
        return str(self.start_date_of_shift)

    def get_str_end_date(self):
        return str(self.end_date_of_shift)
