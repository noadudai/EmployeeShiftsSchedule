import uuid
from abc import abstractmethod
from dataclasses import dataclass, field

from models.shifts.shift import Shift


class ShiftsPreferences:

    @abstractmethod
    def get_shifts_preferences(self, shifts: list[Shift]) -> list[Shift]:
        pass
