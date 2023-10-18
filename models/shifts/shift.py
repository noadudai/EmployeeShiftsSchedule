from .shifts_enum import ShiftTypesEnum
from datetime import datetime


class Shift:

    def __init__(self, shift_type: ShiftTypesEnum, start_date_and_time_of_shift: datetime, end_date_and_time_of_shift: datetime):
        self.type = shift_type
        self.employee = None
        self.start_date_and_time_of_shift = start_date_and_time_of_shift
        self.end_date_and_time_of_shift = end_date_and_time_of_shift

    # Setting the employee that will work this shift after the schedule has been created
    def set_employee(self, employee):
        self.employee = employee
