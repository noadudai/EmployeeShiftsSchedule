from dataclasses import dataclass, field

from .day_preference import DayOffPreference
from .shift_preference_by_id import ShiftsPreferenceById
from .shifts_preference import ShiftsPreference


@dataclass
class Preferences:
    days_cannot_work: list[DayOffPreference] = field(default_factory=list)
    days_prefer_not_to_work: list[DayOffPreference] = field(default_factory=list)
    shifts_prefer_to_work_in_days: list[ShiftsPreference] = field(default_factory=list)
    shifts_cannot_work: list[ShiftsPreference] = field(default_factory=list)
    shifts_has_to_work_by_id: list[ShiftsPreferenceById] = field(default_factory=list)
