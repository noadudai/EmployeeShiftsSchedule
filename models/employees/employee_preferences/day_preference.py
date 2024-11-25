import datetime
from dataclasses import dataclass

from models.employees.employee_preferences.shifts_preference import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class DayOffPreference(ShiftsPreferences):
    day_date: datetime.date

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        shifts_in_day_off_preference = [shift for shift in shifts if shift.start_time.date() == self.day_date]

        return shifts_in_day_off_preference
