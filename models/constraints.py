from typing import List
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel

from .employees.employee import Employee
from .shifts.shift import Shift


class Constraints:

    def __init__(self, employees: List[Employee], shifts: list[Shift]):
        self.employees = employees
        self.cp_model = cp_model.CpModel()
        self.shifts = shifts
        self.all_possible_shift_employee_combinations = self._generate_all_possible_shift_employee_combinations(self.employees, self.shifts, self.cp_model)

    @staticmethod
    def _generate_all_possible_shift_employee_combinations(employees: List[Employee], shifts: list[Shift], cp_model):
        all_possible_shift_employee_combinations = {}
        for employee in employees:
            for shift in shifts:
                all_possible_shift_employee_combinations[
                    (employee.id, str(shift.start_date_and_time_of_shift.date()),
                     str(shift.end_date_and_time_of_shift.date()), shift.type.value)
                ] = cp_model.NewBoolVar(
                        f"shift_employee{employee.id}_shift_start_date{str(shift.start_date_and_time_of_shift.date())}_shift_end_date{str(shift.end_date_and_time_of_shift.date())}_shift{shift.type.value}")

        return all_possible_shift_employee_combinations

    # A constraint that ensures that there will be only one employee in each shift per day

    def add_only_one_employee_in_each_shift_constraint(self):
        for shift in self.shifts:
            self.cp_model.AddExactlyOne(self.all_possible_shift_employee_combinations[(employee.id, str(shift.start_date_and_time_of_shift.date()), str(shift.end_date_and_time_of_shift.date()),shift.type.value)] for employee in self.employees)

    # A constraint that ensures that each employee works at most one shift per day
    def add_at_most_one_shift_that_starts_in_the_same_day_constraint(self):

        days_in_the_given_shift_list = list(set(str(shift.start_date_and_time_of_shift.date()) for shift in self.shifts))

        for day in days_in_the_given_shift_list:
            for employee in self.employees:
                # a list of all the shifts that the employee is working on that day
                shifts_on_day = []

                for shift in self.shifts:
                    if str(shift.start_date_and_time_of_shift.date()) == day:
                        shifts_on_day.append(
                            self.all_possible_shift_employee_combinations[(employee.id, str(shift.start_date_and_time_of_shift.date()), str(shift.end_date_and_time_of_shift.date()), shift.type.value)])
                self.cp_model.AddAtMostOne(shifts_on_day)

    # A constraint that ensures that on a given day, there are is no new employee in evening shift and a new employee
    # in closing shift, and in the weekends, no 2 new employee in morning and backup shifts.
    def add_constraint_to_prevent_new_employees_working_together(self):
        pass

    # A constraint that ensures that each employee does not work more than 6 days in a week
    def add_no_more_that_6_working_days_a_week_constraint(self):
        pass

    # A constraint that ensures that only an employee who asked for a day-off in advance will get that day off.
    # And if not, the solver will assign an employee based on needs.
    def add_employee_day_off_request_constraint(self):
        pass

    # A constraint that ensures that an employee how is working on a closing shift,
    # will not work a morning shift on the day after.
    def add_no_opening_shift_after_closing_shift_constraint(self):
        pass

    def objective_function(self):
        solver = cp_model.CpSolver()
        status = solver.Solve(self.cp_model)
        if status == cp_model.OPTIMAL:
            for shift in self.shifts:
                for employee in self.employees:
                    if solver.Value(self.all_possible_shift_employee_combinations[(
                            employee.id, str(shift.start_date_and_time_of_shift.date()),
                            str(shift.end_date_and_time_of_shift.date()),
                            shift.type.value)]):
                        print(
                            f"Shift {shift.type.value} on day {shift.start_date_and_time_of_shift.date()} starts at: {shift.start_date_and_time_of_shift},"
                            f" employee working that shift: {employee.name}.")
        else:
            print("No optimal solution found !")
