from typing import List

from Models.Day_model import DayModel


class WeekModel:

    def __init__(self, days_in_this_week: List[DayModel]):
        self.days_in_this_week = days_in_this_week
