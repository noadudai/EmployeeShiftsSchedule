from enum import Enum
from typing import List

from Models.Day_model import DayModel


#  Priority levels
class PriorityEnum(Enum):
    HIGHEST = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    LOWEST = 1


class EmployeeModel:

    def __init__(self, name: str, priority: PriorityEnum, is_new: bool, preferences: List[DayModel]):
        self.name = name
        self.priority = priority
        self.is_new = is_new
        self.preferences = preferences

    def update_priority(self, new_priority: PriorityEnum):
        self.priority = new_priority

    def update_status(self, status: bool):
        self.is_new = status

    def update_preferences(self, new_preferences: List[DayModel]):
        self.preferences = new_preferences
