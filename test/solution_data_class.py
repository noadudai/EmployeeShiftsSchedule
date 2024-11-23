from dataclasses import dataclass

from ortools.sat.python.cp_model import IntVar


# @dataclass
# class Solutions:
#     # Each solution is a key IntVar as a string and value as the value of that IntVar as an int
#     optimal_solutions: list[dict[str, int]]
#
@dataclass
class Solution:
    optimal_solution: dict[str, int]
    variables: dict[str, int]
