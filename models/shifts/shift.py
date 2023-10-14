from .shifts_enum import ShiftsEnum


class Shift:

    def __init__(self, shift_type: ShiftsEnum):
        self.type = shift_type
        self.employee = None

    # Setting the employee that will work this shift
    def set_employee(self, employee):
        self.employee = employee
