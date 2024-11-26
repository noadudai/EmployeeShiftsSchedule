import uuid
from dataclasses import dataclass, field

from models.employees.employee_preferences.shifts_preference import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class ShiftPreferencesById(ShiftsPreferences):
    shift_prefs_by_id: list[uuid] = field(default_factory=list)

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        shifts = [shift for shift in shifts if shift.shift_id in self.shift_prefs_by_id]

        return shifts
