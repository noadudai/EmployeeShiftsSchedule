from .shifts_enum import ShiftTypesEnum
from datetime import datetime


class Shift:

    def __init__(self, shift_type: ShiftTypesEnum, start_date_and_time_of_shift: datetime, end_date_and_time_of_shift: datetime):
        self.type = shift_type
        self.start_date_and_time_of_shift = start_date_and_time_of_shift
        self.end_date_and_time_of_shift = end_date_and_time_of_shift

    # # A function to return a string representing the start date of the given shift
    def get_str_start_date_from_shift(self):
        return str(self.start_date_and_time_of_shift.date())

    # A function to return a string representing the end date of the given shift
    def get_str_end_date_from_shift(self):
        return str(self.end_date_and_time_of_shift.date())

    # A function to return the start date of the given shift
    def get_start_date_of_shift(self):
        return self.start_date_and_time_of_shift.date()

    # A function to return the end date of the given shift
    def get_end_date_of_shift(self):
        return self.end_date_and_time_of_shift.date()
