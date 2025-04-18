from dataclasses import dataclass

from src.models.employees.employee_preferences.shifts_preference import ShiftsPreference
from src.models.shifts.shift import Shift


@dataclass
class NoPreference(ShiftsPreference):

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        return[]
