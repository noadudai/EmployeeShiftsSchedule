from dataclasses import field
from typing import List

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from test.solution_data_class import Solution


class ScheduleSolutionCollector(cp_model.CpSolverSolutionCallback):

    def __init__(self, emp_shift_assignments: List[IntVar], variables: List[IntVar] = []):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution = emp_shift_assignments
        self.__schedule_solutions: List[Solution] = []

    def on_solution_callback(self):
        self.__solution_count += 1

        solution: dict[str, int] = {}
        vars: dict[str, int] = {}

        for v in self.__variables:
            vars[f"{v}"] = self.Value(v)
        for s in self.__solution:
            solution[f"{s}"] = self.Value(s)

        self.__schedule_solutions.append(Solution(solution, vars))

    def solution_count(self):
        return self.__solution_count

    def get_solutions(self):
        return self.__schedule_solutions
