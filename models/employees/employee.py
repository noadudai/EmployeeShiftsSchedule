from dataclasses import dataclass
import uuid

from .employee_position_enum import EmployeePositionEnum
from .employee_preferences.preferences import Preferences
from .employee_priority_enum import EmployeePriorityEnum
from .employee_status_enum import EmployeeStatusEnum


@dataclass
class Employee:
    name: str
    priority: EmployeePriorityEnum
    employee_status: EmployeeStatusEnum
    employee_id: uuid.UUID
    position: EmployeePositionEnum
    preferences: Preferences
