import uuid

import pydantic
from pydantic import Field

from src.models.solution.pydantic_config import ConfigPydanticDataclass


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class ScheduleSolutionMetadata:
    number_of_closings_for_each_emp: dict[uuid.UUID | str, int]
    number_of_mornings_for_each_emp:  dict[uuid.UUID | str, int]
    number_of_shift_for_each_emp: dict[uuid.UUID | str, int]

    # shift id, employee id
    schedule: dict[str, str]
