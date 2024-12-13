import uuid
from dataclasses import dataclass, field

from src.models.employees.employee_preferences.shifts_preference import ShiftsPreference
from src.models.shifts.shift import Shift


@dataclass
class ShiftIdPreference(ShiftsPreference):
    shifts_pref_by_id: list[uuid] = field(default_factory=list)

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        shifts = [shift for shift in shifts if shift.shift_id in self.shifts_pref_by_id]

        return shifts
