from enum import Enum


class EmployeeStatusEnum(Enum):
    NEW_EMPLOYEE = "NEW_EMPLOYEE"               # A new employee
    JUNIOR_EMPLOYEE = "JUNIOR_EMPLOYEE"         # A not so new employee
    MID_LEVEL_EMPLOYEE = "MID_LEVEL_EMPLOYEE"   # An experienced employee
    SENIOR_EMPLOYEE = "SENIOR_EMPLOYEE"         # An experienced and highly skilled employee
 