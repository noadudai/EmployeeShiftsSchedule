import pydantic.dataclasses

from src.models.employees.employee import Employee
from src.models.shifts.shift import Shift
from src.models.solution.one_schedule_solution_metadata import ScheduleSolutionMetadata
from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class SchedulesAndEmpsMetadata:
    schedules: list[ScheduleSolutionMetadata]
    employees: list[Employee]
    shifts: list[Shift]
