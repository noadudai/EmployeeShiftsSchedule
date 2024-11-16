import uuid
from dataclasses import dataclass, field

from models.shifts.shift import Shift


@dataclass
class ShiftsPreference:
    shift_prefs_by_id: list[uuid.UUID] = field(default_factory=list)

    def get_shifts(self, shifts: list[Shift]) -> list[Shift]:
        shifts = [shift for shift in shifts if shift.shift_id in self.shift_prefs_by_id]

        return shifts
