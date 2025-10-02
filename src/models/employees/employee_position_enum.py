from enum import Enum

EmployeePositionDict = {
    "PART_TIMER": 1,
    "FULL_TIMER": 3
}


class EmployeePositionEnum(str, Enum):
    PART_TIMER = "PART_TIMER"
    FULL_TIMER = "FULL_TIMER"
