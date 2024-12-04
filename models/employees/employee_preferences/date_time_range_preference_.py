import datetime
from dataclasses import dataclass

from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.shifts.shift import Shift


@dataclass
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
