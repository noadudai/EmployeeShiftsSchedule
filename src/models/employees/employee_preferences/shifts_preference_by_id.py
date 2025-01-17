import uuid
from dataclasses import field

import pydantic

from src.models.employees.employee_preferences.shifts_preference import ShiftsPreference
from src.models.shifts.shift import Shift
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ShiftIdPreference(ShiftsPreference):
    shifts_pref_by_id: list[uuid] = field(default_factory=list)

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        shifts = [shift for shift in shifts if shift.shift_id in self.shifts_pref_by_id]

        return shifts
