from datetime import timedelta
from typing import List
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel

from .employees.employee import Employee
from .employees.employee_status_enum import EmployeeStatusEnum
from .shifts.shift import Shift
from .shifts.shifts_enum import ShiftTypesEnum


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
            self.cp_model.AddExactlyOne(self.all_possible_shift_employee_combinations[
                                            (employee.id,
                                             str(shift.start_date_and_time_of_shift.date()),
                                             str(shift.end_date_and_time_of_shift.date()),
                                             shift.type.value)]
                                        for employee in self.employees)

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
                            self.all_possible_shift_employee_combinations[
                                (employee.id,
                                 str(shift.start_date_and_time_of_shift.date()),
                                 str(shift.end_date_and_time_of_shift.date()),
                                 shift.type.value)])
                self.cp_model.AddAtMostOne(shifts_on_day)

    # A constraint that ensures that on each day,
    def add_constraint_to_prevent_new_employees_working_together(self, first_shift: ShiftTypesEnum, second_shift:ShiftTypesEnum):
        days_in_the_given_shift_list = list(set(str(shift.start_date_and_time_of_shift.date()) for shift in self.shifts))

        for day in days_in_the_given_shift_list:
            # collecting all the new employees that are working on this day is specific shifts.
            new_employees_on_first_shift = []
            new_employees_on_second_shift = []

            for employee in self.employees:
                for shift in self.shifts:
                    if str(shift.start_date_and_time_of_shift.date()) == day and shift.type == first_shift and employee.status == EmployeeStatusEnum.new_employee:
                        new_employees_on_first_shift.append(self.all_possible_shift_employee_combinations[
                                (employee.id,
                                 str(shift.start_date_and_time_of_shift.date()),
                                 str(shift.end_date_and_time_of_shift.date()),
                                 shift.type.value)])

                    if str(shift.start_date_and_time_of_shift.date()) == day and shift.type == second_shift and employee.status == EmployeeStatusEnum.new_employee:
                        new_employees_on_second_shift.append(self.all_possible_shift_employee_combinations[
                                (employee.id,
                                 str(shift.start_date_and_time_of_shift.date()),
                                 str(shift.end_date_and_time_of_shift.date()),
                                 shift.type.value)])

            # The solver will try different combinations of values for these booleans while exploring the solution space
            # to find a valid assignment of employees to shifts that satisfies all constraints
            condition_shift1 = self.cp_model.NewBoolVar(f"condition_shift1_{day}")
            condition_shift2 = self.cp_model.NewBoolVar(f"condition_shift2_{day}")

            # if there's at least one new employee on shift1, condition_shift1 must be true,
            # and if there's no new employee on shift1, condition_shift1 must be false.
            self.cp_model.Add(sum(new_employees_on_first_shift) >= 1).OnlyEnforceIf(condition_shift1)
            self.cp_model.Add(sum(new_employees_on_first_shift) == 0).OnlyEnforceIf(condition_shift1.Not())

            self.cp_model.Add(sum(new_employees_on_second_shift) >= 1).OnlyEnforceIf(condition_shift2)
            self.cp_model.Add(sum(new_employees_on_second_shift) == 0).OnlyEnforceIf(condition_shift2.Not())

            # Implication: if there's a new employee on shift1, there cannot be a new employee on shift2
            self.cp_model.AddBoolOr([condition_shift1.Not(), condition_shift2.Not()])

    # A constraint that ensures that each employee does not work more than 6 days in a week
    def add_no_more_that_6_working_days_a_week_constraint(self):
        # The max working days for an employee in a week is 6 by law.
        max_working_days_in_a_week = 6

        # Count the shifts an employee is assigned to.
        total_shifts_worked = {}

        for employee in self.employees:
            total_shifts_worked[employee.id] = sum(self.all_possible_shift_employee_combinations[(
                employee.id,
                str(shift.start_date_and_time_of_shift.date()),
                str(shift.end_date_and_time_of_shift.date()),
                shift.type.value)
            ] for shift in self.shifts)

        # ensure that the total shifts worked by each employee is not more than 6.
        for employee in self.employees:
            self.cp_model.Add(total_shifts_worked[employee.id] <= max_working_days_in_a_week)

    # A constraint that ensures that only an employee who asked for a day-off in advance will get that day off.
    # And if not, the solver will assign an employee based on needs.
    def add_employee_day_off_request_constraint(self):
        pass

    # A constraint that ensures that an employee how is working on a closing shift,
    # will not work a morning shift on the day after.
    def add_no_morning_shift_after_closing_shift_constraint(self):
        for employee in self.employees:
            worked_closing_shift_yesterday = self.cp_model.NewBoolVar(f"{employee.name}_worked_closing_shift_yesterday_day")

            # checking for every shift if the shift before was a closing shift
            for shift in range(1, len(self.shifts)):
                if self.shifts[shift - 1].type == ShiftTypesEnum.CLOSING:

                    # setting worked_closing_shift_yesterday to be 1 or 0 according to the working employee
                    self.cp_model.Add(worked_closing_shift_yesterday == self.all_possible_shift_employee_combinations.get(
                        (employee.id,
                         str(self.shifts[shift - 1].start_date_and_time_of_shift.date()),
                         str(self.shifts[shift - 1].end_date_and_time_of_shift.date()),
                         self.shifts[shift-1].type.value), 0))

                    self.cp_model.Add(self.all_possible_shift_employee_combinations[
                                          (employee.id,
                                           str(self.shifts[shift].start_date_and_time_of_shift.date()),
                                           str(self.shifts[shift].end_date_and_time_of_shift.date()),
                                           self.shifts[shift].type.value)] == 0).OnlyEnforceIf(
                        (self.shifts[shift].start_date_and_time_of_shift.date() - self.shifts[shift].end_date_and_time_of_shift.date()) >= timedelta(hours=24))

    def objective_function(self):
        # maximize on priority and preferences of the employees
        solver = cp_model.CpSolver()
        status = solver.Solve(self.cp_model)
        print(status)
        print(cp_model.OPTIMAL)
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
                        break
        else:
            print("No optimal solution found !")
