from enum import Enum


class ShiftTypesEnum(Enum):
    MORNING = "morning"
    MORNING_BACKUP = "morning backup"
    EVENING = "evening"
    CLOSING = "closing"
    THURSDAY_BACKUP = "thursday backup"
    WEEKEND_MORNING = "weekend morning"
    WEEKEND_MORNING_BACKUP = "weekend morning backup"
    WEEKEND_EVENING_BACKUP = "weekend evening backup"
