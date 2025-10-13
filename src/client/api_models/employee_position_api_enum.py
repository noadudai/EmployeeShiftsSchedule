from enum import Enum


class EmployeePositionApiEnum(str, Enum):
    PART_TIMER = "PART_TIMER"
    FULL_TIMER = "FULL_TIMER"
    