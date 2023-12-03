from enum import Enum


# datetime.weekday() will return an int representing:
class DaysEnum(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6
