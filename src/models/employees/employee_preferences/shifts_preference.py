from abc import abstractmethod

import pydantic

from src.models.shifts.shift import Shift
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ShiftsPreference:

    @abstractmethod
    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        raise NotImplementedError
