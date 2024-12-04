from dataclasses import dataclass, field

from models.employees.employee_preferences.shifts_preferences import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class CombinePreferences(ShiftsPreferences):
    preferences: list[ShiftsPreferences] = field(default_factory=list)

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        all_shifts_in_preferences = []

        for preference in self.preferences:
            all_shifts_in_preferences.extend(preference.get_shifts_preferences(shifts))

        return all_shifts_in_preferences
