from dataclasses import dataclass

from models.solution.one_schedule_solution import Solution


@dataclass
class ScheduleSolutions:
    solutions: list[Solution]
