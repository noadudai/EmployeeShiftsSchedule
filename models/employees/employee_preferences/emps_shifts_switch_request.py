import uuid
from dataclasses import dataclass


@dataclass
class EmployeesShiftSwitchRequest:
    emp_1_id: uuid
    emp_1_has_shift: uuid
    emp_2_id: uuid
    emp_2_has_shift: uuid
