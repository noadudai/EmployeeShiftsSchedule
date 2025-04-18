import pydantic

from src.models.employees.employee_preferences.shifts_preference import ShiftsPreference
from src.models.shifts.shift import Shift
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class NoPreference(ShiftsPreference):

    def get_shifts_preference(self, shifts: list[Shift]) -> list[Shift]:
        return[]
