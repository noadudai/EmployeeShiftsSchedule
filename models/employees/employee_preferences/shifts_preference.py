import uuid
from abc import abstractmethod
from dataclasses import dataclass, field

from models.shifts.shift import Shift


class ShiftsPreference:

    @abstractmethod
    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        raise NotImplementedError
