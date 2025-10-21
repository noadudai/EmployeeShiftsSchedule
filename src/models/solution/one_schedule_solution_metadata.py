import uuid
from typing import List

import pydantic

from src.models.solution.number_of_shifts_assigned_to_employee import NumberOfShiftsAssignedToEmployee
from src.models.solution.pydantic_config import ConfigPydanticDataclass
from src.models.solution.schedule_shift_assignment import ScheduleShiftAssignment


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ScheduleSolutionMetadata:
    number_of_closings_for_each_emp: List[NumberOfShiftsAssignedToEmployee]
    number_of_mornings_for_each_emp:  List[NumberOfShiftsAssignedToEmployee]
    number_of_shift_for_each_emp: List[NumberOfShiftsAssignedToEmployee]

    schedule: List[ScheduleShiftAssignment]
