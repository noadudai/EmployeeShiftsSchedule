from dataclasses import dataclass

from models.solution.one_schedule_solution import ScheduleSolution


@dataclass
class ScheduleSolutions:
    solutions: list[ScheduleSolution]
