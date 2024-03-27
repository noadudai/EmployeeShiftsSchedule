from dataclasses import dataclass

from .day_preference import DayPreference
from .shifts_preference import ShiftsPreference


@dataclass
class Preferences:
    days_cannot_work: list[DayPreference]
    days_prefer_not_to_work: list[DayPreference]
    shifts_prefer_to_work_in_days: list[ShiftsPreference]
