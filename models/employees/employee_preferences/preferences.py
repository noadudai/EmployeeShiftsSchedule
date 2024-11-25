from dataclasses import dataclass, field

from .day_preference import DayOffPreference
from .shift_preferences_by_id import ShiftPreferencesById


@dataclass
class Preferences:
    days_cannot_work: list[DayOffPreference] = field(default_factory=list)
    days_prefer_not_to_work: list[DayOffPreference] = field(default_factory=list)
    shifts_prefer_by_id: ShiftPreferencesById = field(default_factory=ShiftPreferencesById)
    shifts_cannot_work: ShiftPreferencesById = field(default_factory=ShiftPreferencesById)
