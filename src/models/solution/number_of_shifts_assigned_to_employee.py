import pydantic.dataclasses

from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class NumberOfShiftsAssignedToEmployee:
    employee_id: str
    number_of_shifts: int
