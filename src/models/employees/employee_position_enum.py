from enum import Enum

EmployeePositionValue = {
    "PART_TIMER": 1,
    "FULL_TIMER": 3
}


class EmployeePositionEnum(Enum):
    PART_TIMER = "PART_TIMER"
    FULL_TIMER = "FULL_TIMER"
