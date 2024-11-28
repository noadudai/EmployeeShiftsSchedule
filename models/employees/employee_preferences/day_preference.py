import datetime
from dataclasses import dataclass, field

from models.employees.employee_preferences.shifts_preference import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class DayOffPreference(ShiftsPreferences):
    day_date: list[datetime.date] = field(default_factory=list)

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        shifts_in_day_offs_preference = []

        for day in self.day_date:
            for shift in shifts:
                if shift.start_time.date() == day:
                    shifts_in_day_offs_preference.append(shift)

        return shifts_in_day_offs_preference
