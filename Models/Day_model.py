from enum import Enum


class DaysEnum(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class DayModel:

    def __init__(self, day_of_the_week, shifts):
        self.today_is = day_of_the_week
        self.shifts = shifts
