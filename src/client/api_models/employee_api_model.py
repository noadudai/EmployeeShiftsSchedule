from dataclasses import dataclass, field

from src.client.api_models.employee_position_api_enum import EmployeePositionApiEnum
from src.client.api_models.employee_priority_api_enum import EmployeePriorityApiEnum
from src.client.api_models.employee_status_api_enmu import EmployeeStatusApiEnum
from src.client.api_models.shift_types_api_enum import ShiftTypesApiEnum
from src.models.employees.employee_preferences.employees_shifts_preferences import EmployeesShiftsPreferences


@dataclass
class EmployeeApiModel:
    name: str
    priority: EmployeePriorityApiEnum
    employee_status: EmployeeStatusApiEnum
    employee_id: str
    position: EmployeePositionApiEnum
    shift_types_trained_to_do: list[ShiftTypesApiEnum]
    shifts_preferences: EmployeesShiftsPreferences = field(default_factory=EmployeesShiftsPreferences)
