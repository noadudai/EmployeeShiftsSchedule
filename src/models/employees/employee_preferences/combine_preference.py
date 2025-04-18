from dataclasses import field, dataclass
from typing import Union

import pydantic

from .date_time_range_preference_ import DateTimeRangePreference
from .shifts_preference import ShiftsPreference
from .shifts_preference_by_id import ShiftIdPreference
from src.models.shifts.shift import Shift
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class CombinePreference(ShiftsPreference):
    preferences: list[Union[DateTimeRangePreference, ShiftIdPreference]] = field(default_factory=list)

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        all_shifts_in_preferences = []

        for preference in self.preferences:
            all_shifts_in_preferences.extend(preference.get_shifts_preference(shifts))

        return all_shifts_in_preferences
