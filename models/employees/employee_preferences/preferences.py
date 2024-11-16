from dataclasses import dataclass, field

from .day_preference import DayOffPreference
from .shifts_preference import ShiftsPreference


@dataclass
class Preferences:
    days_cannot_work: list[DayOffPreference] = field(default_factory=list)
    days_prefer_not_to_work: list[DayOffPreference] = field(default_factory=list)
    shifts_prefer_to_work_in_days: ShiftsPreference = field(default_factory=ShiftsPreference)
    shifts_cannot_work: ShiftsPreference = field(default_factory=ShiftsPreference)
