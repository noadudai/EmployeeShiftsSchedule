from dataclasses import dataclass, field

from models.employees.employee_preferences.combine_preference import CombinePreference
from models.employees.employee_preferences.no_preferences import NoPreference
from models.employees.employee_preferences.shifts_preference import ShiftsPreference


@dataclass
class EmployeesShiftsPreferences:
    shifts_cannot_work: ShiftsPreference = field(default_factory=NoPreference)
    shifts_prefer_not_to_work: ShiftsPreference = field(default_factory=NoPreference)
    shifts_wants_to_work: ShiftsPreference = field(default_factory=NoPreference)
