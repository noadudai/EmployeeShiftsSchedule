from dataclasses import dataclass

from .employee_priority_enum import EmployeePriorityEnum
from .employee_status_enum import EmployeeStatusEnum


@dataclass
class Employee:
    name: str                                   # the name of the employee
    employee_priority: EmployeePriorityEnum     # the priority of the employee
    is_new: EmployeeStatusEnum                  # the status of the employee
    id: int                                     # the employee id
