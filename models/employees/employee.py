from dataclasses import dataclass, field
import uuid

from .employee_position_enum import EmployeePositionEnum
from .employee_preferences.preferences import Preferences
from .employee_priority_enum import EmployeePriorityEnum
from .employee_status_enum import EmployeeStatusEnum
from ..shifts.shifts_types_enum import ShiftTypesEnum


@dataclass
class Employee:
    name: str
    priority: EmployeePriorityEnum = EmployeePriorityEnum.LOW
    employee_status: EmployeeStatusEnum = EmployeeStatusEnum.mid_level_employee
    employee_id: uuid.UUID = uuid.uuid4()
    position: EmployeePositionEnum = EmployeePositionEnum.full_timer
    preferences: Preferences = field(default_factory=Preferences)
    shift_types_trained_to_do: list[ShiftTypesEnum] = field(default_factory=list)
3