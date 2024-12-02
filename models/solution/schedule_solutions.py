from dataclasses import dataclass

from models.solution.one_schedule_solution_metadata import ScheduleSolutionMetadata


@dataclass
class ScheduleSolutions:
    solutions: list[ScheduleSolutionMetadata]
