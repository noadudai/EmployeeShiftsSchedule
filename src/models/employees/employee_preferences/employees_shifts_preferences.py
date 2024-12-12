from dataclasses import field

import pydantic

from src.models.employees.employee_preferences.no_preferences import NoPreference
from src.models.employees.employee_preferences.shifts_preference import ShiftsPreference
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class EmployeesShiftsPreferences:
    shifts_cannot_work: ShiftsPreference = field(default_factory=NoPreference)
    shifts_prefer_not_to_work: ShiftsPreference = field(default_factory=NoPreference)
    shifts_wants_to_work: ShiftsPreference = field(default_factory=NoPreference)
