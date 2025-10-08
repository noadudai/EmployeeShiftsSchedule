from enum import Enum

EmployeePositionValue = {
    "PartTimer": 1,
    "FullTimer": 3
}


class EmployeePositionEnum(Enum):
    PART_TIMER = "PartTimer"
    FULL_TIMER = "FullTimer"
