from enum import Enum


EmployeePriorityValue = {
    "HIGHEST": 5,
    "HIGH": 4,
    "MEDIUM": 3,
    "LOW": 2,
    "LOWEST": 1
}


class EmployeePriorityEnum(Enum):
    HIGHEST = "HIGHEST"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    LOWEST = "LOWEST"
