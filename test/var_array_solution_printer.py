from typing import List

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from test.solution_data_class import Solutions


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables: List[IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solutions = Solutions([])

    def on_solution_callback(self):
        self.__solution_count += 1
        solution: dict[str, int] = {}
        for v in self.__variables:
            solution[f"{v}"] = self.Value(v)
        self.__solutions.optimal_solutions.append(solution)

    def solution_count(self):
        return self.__solution_count

    def get_solutions(self):
        return self.__solutions
