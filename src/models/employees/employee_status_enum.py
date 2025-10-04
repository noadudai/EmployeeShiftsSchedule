from enum import Enum


class EmployeeStatusEnum(Enum):
    new_employee = "NEW_EMPLOYEE"               # A new employee
    junior_employee = "JUNIOR_EMPLOYEE"         # A not so new employee
    mid_level_employee = "MID_LEVEL_EMPLOYEE"   # An experienced employee
    senior_employee = "SENIOR_EMPLOYEE"         # An experienced and highly skilled employee
 