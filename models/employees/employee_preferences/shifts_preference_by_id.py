import uuid
from dataclasses import dataclass, field

from models.employees.employee_preferences.shifts_preferences import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class ShiftIdPreference(ShiftsPreferences):
    shifts_pref_by_id: list[uuid] = field(default_factory=list)

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        shifts = [shift for shift in shifts if shift.shift_id in self.shifts_pref_by_id]

        return shifts
