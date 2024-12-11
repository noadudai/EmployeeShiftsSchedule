import pydantic.dataclasses
from pydantic import BaseModel

from models.employees.employee import Employee
from models.shifts.shift import Shift
from models.solution.one_schedule_solution_metadata import ScheduleSolutionMetadata
from models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class SchedulesAndEmpsMetadata:
    schedules: list[ScheduleSolutionMetadata]
    employees: list[Employee]
    shifts: list[Shift]
