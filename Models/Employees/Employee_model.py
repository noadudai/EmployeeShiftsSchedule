from dataclasses import dataclass
from typing import List

from Models.Day_related.Day_model import Day
from Models.Employee_related.Employee_priority_enum import EmployeePriorityEnum
from Models.Employee_related.Employee_status_enum import EmployeeStatusEnum


@dataclass
class Employee:
    name: str                                   # the name of the employee
    employee_priority: EmployeePriorityEnum     # the priority of the employee
    is_new: EmployeeStatusEnum                  # the status of the employee
    preferences: List[Day]                      # a list of the employees shifts preferences
