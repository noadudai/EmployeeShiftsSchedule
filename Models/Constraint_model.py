from typing import List

from ortools.sat.python import cp_model

from Models.Employee_model import EmployeeModel
from Models.Week_model import WeekModel


class ConstraintModel:

    def __init__(self, week_info: WeekModel, employees: List[EmployeeModel]):
        self.week_info = week_info
        self.employees = employees
        self.cp_model = cp_model.CpModel()
        self.all_possible_shifts_combo = {}
