import datetime

import pydantic

from src.models.employees.employee_preferences.shifts_preference import ShiftsPreference
from src.models.shifts.shift import Shift
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class DateTimeRangePreference(ShiftsPreference):
    range_start: datetime.datetime
    range_end: datetime.datetime

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        shifts_inside_range_day_preference = []

        for shift in shifts:

            if self.range_start >= shift.start_time >= self.range_end or \
                    self.range_start >= shift.end_time >= self.range_end or\
                    self.range_start <= shift.start_time <= self.range_end:
                shifts_inside_range_day_preference.append(shift)

        return shifts_inside_range_day_preference
