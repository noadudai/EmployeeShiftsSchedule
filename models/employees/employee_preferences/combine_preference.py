from dataclasses import dataclass, field

from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.shifts.shift import Shift


@dataclass
class CombinePreference(ShiftsPreference):
    preferences: list[ShiftsPreference] = field(default_factory=list)

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        all_shifts_in_preferences = []

        for preference in self.preferences:
            all_shifts_in_preferences.extend(preference.get_shifts_preference(shifts))

        return all_shifts_in_preferences
