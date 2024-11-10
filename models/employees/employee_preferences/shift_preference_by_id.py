import uuid
from dataclasses import dataclass


@dataclass
class ShiftsPreferenceById:
    shift_id: uuid.UUID
