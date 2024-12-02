from dataclasses import dataclass, field

from .days_preference import DaysPreference
from .shift_preferences_by_id import ShiftPreferencesById


@dataclass
class Preferences:
    days_cannot_work: DaysPreference = field(default_factory=DaysPreference)
    days_prefer_not_to_work: DaysPreference = field(default_factory=DaysPreference)
    shifts_prefer_by_id: ShiftPreferencesById = field(default_factory=ShiftPreferencesById)
    shifts_cannot_work: ShiftPreferencesById = field(default_factory=ShiftPreferencesById)
