import uuid
from dataclasses import dataclass


@dataclass
class Solution:
    number_of_closings_for_each_emp: dict[uuid.uuid4(), int]
    number_of_mornings_for_each_emp:  dict[uuid.uuid4(), int]
    number_of_shift_for_each_emp: dict[uuid.uuid4(), int]
    schedule: dict[uuid.uuid4(), uuid.uuid4()]
