import uuid
from abc import abstractmethod
from dataclasses import dataclass, field

import pydantic

from models.shifts.shift import Shift
from models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ShiftsPreference:

    @abstractmethod
    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        raise NotImplementedError
