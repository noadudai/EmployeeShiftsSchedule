import pydantic.dataclasses

from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ScheduleShiftAssignment:
    shift_id: str
    employee_id: str
