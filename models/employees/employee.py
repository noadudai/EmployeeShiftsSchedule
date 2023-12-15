from uuid import uuid4

from .employee_priority_enum import EmployeePriorityEnum
from .employee_status_enum import EmployeeStatusEnum


class Employee:
    def __init__(self, name: str, employee_priority: EmployeePriorityEnum, employee_status: EmployeeStatusEnum):
        self.name = name
        self.priority = employee_priority
        self.status = employee_status
        # Generates a random UUID
        self.id = uuid4()
