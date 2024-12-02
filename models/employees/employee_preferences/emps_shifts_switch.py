import uuid
from dataclasses import dataclass


@dataclass
class EmployeesShiftsSwitch:
    emp_who_wnats_to_switch_id: uuid
    emp_who_wnats_to_switch_has_shift: uuid
    emp_who_wnats_to_switch_wants_shift: uuid
    emp_to_switch_with_id: uuid
    emp_to_switch_with_has_shift: uuid
    emp_to_switch_with_wants_shift: uuid
