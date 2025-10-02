import pydantic

from src.models.employees.employee import Employee
from src.models.shifts.shift import Shift
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ScheduleCreationData:
    employees: list[Employee]
    shifts: list[Shift]
    number_of_schedules: int
