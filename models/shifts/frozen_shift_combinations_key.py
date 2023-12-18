from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class FrozenShiftCombinationsKey:
    employee_id: uuid4
    shift_id: uuid4
