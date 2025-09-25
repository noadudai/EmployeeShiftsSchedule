from enum import Enum


class EmployeePositionEnum(str, Enum):
    PART_TIMER = "part_timer"
    FULL_TIMER = "full_timer"

    @property
    def shifts(self) -> int:
        if self == EmployeePositionEnum.PART_TIMER:
            return 1
        elif self == EmployeePositionEnum.FULL_TIMER:
            return 3
