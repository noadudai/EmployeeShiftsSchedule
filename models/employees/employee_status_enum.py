from enum import Enum


class EmployeeStatusEnum(Enum):
    new_employee = "new employee"               # A new employee
    junior_employee = "junior employee"         # A not so new employee
    mid_level_employee = "mid level employee"   # An experienced employee
    senior_employee = "senior employee"         # An experienced and highly skilled employee
 