import datetime
from dataclasses import dataclass

from models.employees.employee_preferences.shifts_preference import ShiftsPreferences
from models.shifts.shift import Shift


@dataclass
class DaysRangePreference(ShiftsPreferences):
    date_range_start: datetime.datetime
    date_range_end: datetime.datetime

    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        shifts_inside_range_day_preference = []
        dates_in_range = [self.date_range_start.date() + datetime.timedelta(days=day) for day in
                          range(((self.date_range_start.date() - self.date_range_end.date()).days) + 1)]

        for shift in shifts:

            shift_starts_before_start_range_and_ends_after_start_range = shift.start_time < self.date_range_start and shift.end_time > self.date_range_start
            shift_starts_after_start_range_and_ends_before_end_of_range = shift.start_time > self.date_range_start and shift.end_time < self.date_range_end
            shift_starts_before_end_range_and_ends_after_end_of_range = shift.start_time < self.date_range_end and shift.end_time > self.date_range_end

            shifts_start_date_in_the_range = shift.start_time.date() in dates_in_range
            shift_end_date_in_the_range = shift.end_time.date() in dates_in_range

            if shifts_start_date_in_the_range or shift_end_date_in_the_range:
                if shift_starts_before_start_range_and_ends_after_start_range or \
                        shift_starts_after_start_range_and_ends_before_end_of_range or \
                        shift_starts_before_end_range_and_ends_after_end_of_range:
                    shifts_inside_range_day_preference.append(shift)

        return shifts_inside_range_day_preference
