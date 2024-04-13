import uuid
from dataclasses import dataclass


@dataclass
class ScheduleSolution:
    schedule: dict[uuid.UUID, uuid.UUID]
    employees_number_of_shifts: dict[uuid.UUID, int]
    employees_number_of_closings: dict[uuid.UUID, int]
    employees_number_of_mornings: dict[uuid.UUID, int]
