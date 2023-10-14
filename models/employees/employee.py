from dataclasses import dataclass
from typing import List

from models.days.day import Day
from .employee_priority_enum import EmployeePriorityEnum
from .employee_status_enum import EmployeeStatusEnum


@dataclass
class Employee:
    name: str                                   # the name of the employee
    employee_priority: EmployeePriorityEnum     # the priority of the employee
    is_new: EmployeeStatusEnum                  # the status of the employee
    preferences: List[Day]                      # a list of the employees shifts preferences
