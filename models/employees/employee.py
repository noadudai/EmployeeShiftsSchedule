from dataclasses import dataclass, field
import uuid

from .employee_position_enum import EmployeePositionEnum
from .employee_preferences.preferences import Preferences
from .employee_priority_enum import EmployeePriorityEnum
from .employee_status_enum import EmployeeStatusEnum


@dataclass
class Employee:
    name: str = "test"
    priority: EmployeePriorityEnum = EmployeePriorityEnum.HIGHEST
    employee_status: EmployeeStatusEnum = EmployeeStatusEnum.senior_employee
    employee_id: uuid.UUID = uuid.uuid4()
    position: EmployeePositionEnum = EmployeePositionEnum.full_timer
    preferences: Preferences = field(default_factory=Preferences)
