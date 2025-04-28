from dataclasses import field
from typing import Union

import pydantic

from .combine_preference import CombinePreference
from .date_time_range_preference_ import DateTimeRangePreference
from .no_preferences import NoPreference
from src.models.solution.pydantic_config import ConfigPydanticDataclass
from .shifts_preference_by_id import ShiftIdPreference

PreferenceType = Union[CombinePreference, DateTimeRangePreference, NoPreference, ShiftIdPreference]


@pydantic.dataclasses.dataclass(config=ConfigPydanticDataclass)
class EmployeesShiftsPreferences:
    shifts_cannot_work: PreferenceType = field(default_factory=NoPreference)
    shifts_prefer_not_to_work: PreferenceType = field(default_factory=NoPreference)
    shifts_wants_to_work: PreferenceType = field(default_factory=NoPreference)
