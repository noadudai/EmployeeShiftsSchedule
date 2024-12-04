from dataclasses import dataclass, field

from models.employees.employee_preferences.combine_preference import CombinePreferences
from models.employees.employee_preferences.shifts_preferences import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class CombinedShiftsPreferences(ShiftsPreferences):
    shifts_cannot_work: ShiftsPreferences = field(default_factory=CombinePreferences)
    shifts_prefer_not_to_work: ShiftsPreferences = field(default_factory=CombinePreferences)
    shifts_wants_to_work: ShiftsPreferences = field(default_factory=CombinePreferences)

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        pass
