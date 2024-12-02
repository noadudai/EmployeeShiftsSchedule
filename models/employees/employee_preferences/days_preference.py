from dataclasses import dataclass, field

from models.employees.employee_preferences.days_range_preference_ import DaysRangePreference
from models.employees.employee_preferences.shifts_preference import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class DaysPreference(ShiftsPreferences):
    days: list[DaysRangePreference] = field(default_factory=list)

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        shifts_in_given_dates = []

        for ranged_date in self.days:
            shifts_in_given_dates.extend(ranged_date.get_shifts_preferences(shifts))

        return shifts_in_given_dates

