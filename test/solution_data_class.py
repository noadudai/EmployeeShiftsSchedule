from dataclasses import dataclass, field

from ortools.sat.python.cp_model import IntVar


@dataclass
class Solution:
    optimal_schedule: dict[str, int]
    variables: dict[str, int] = field(default_factory=list)
