import itertools

import pytest
from ortools.sat.python import cp_model

from constraints import generate_new_employees_on_shift, generate_shift_employee_combinations
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift_type import ShiftType
from models.shifts.shifts_types_enum import ShiftTypesEnum
from smaller_constraints import *


def test_add_at_most_one_employee_per_shift_a_day_constrains():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    employees = [test_employee, test_employee2]
    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift], constraint_model)

    for shift in [test_shift]:
        employees_on_shift = [shift_combinations[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)] for employee in employees]
        add_at_most_one_employee_per_shift_a_day_constrains(constraint_model, employees_on_shift)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    start_shift = test_shift.get_str_start_date()
    end_shift = test_shift.get_str_end_date()
    shift_type = test_shift.shift_type.name_of_shift

    assert (status == cp_model.OPTIMAL)

    second_employee_assignment = shift_combinations[(test_employee2.id, start_shift, end_shift, shift_type)]

    expected_employee_working = False
    assert (solver.Value(second_employee_assignment) == expected_employee_working)


# def test_smaller_constraints():
#     constraint_model = cp_model.CpModel()
#     max_working_day = 5
#     shifts_time_diff = datetime.timedelta(hours=12)
#
#     for shift in shifts:
#         employees_on_shift = [shift_combinations[(employee.id, shift.get_str_start_shift, shift.get_str_end_shift, shift.shift_type.name_of_shift.value)] for
#                               employee in employees]
#         add_at_least_one_employee_per_shift_constraint(constraint_model, employees_on_shift)
#
#     for employee in employees:
#         employee_working_days = sum(shift_combinations[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)] for shift in shifts)
#         add_max_working_days_a_week_constraint(employee_working_days, constraint_model, max_working_day)
#
#         for shift_pair in itertools.pairwise(shifts):
#             first_shift, second_shift = shift_pair
#
#             if first_shift.shift_type.name_of_shift == ShiftTypesEnum.CLOSING:
#
#                 datetime_next_shift = datetime.datetime.combine(second_shift.start_date_of_shift, second_shift.shift_type.start_time)
#                 datetime_closing_shift = datetime.datetime.combine(first_shift.end_date_of_shift, first_shift.shift_type.end_time)
#
#                 if datetime_next_shift - datetime_closing_shift <= shifts_time_diff:
#                     add_no_morning_shift_after_closing_shift_constraint(employee, first_shift, second_shift, shift_combinations, constraint_model)
#
#     for day in days:
#         for employee in employees:
#             works_shift_on_day = [shift_combinations[(employee.id, shift.get_str_start_shift, shift.get_str_end_shift, shift.shift_type.name_of_shift.value)] for shift in all_shifts if shift.get_start_date_of_shift == day]
#             add_at_most_one_employee_per_shift_a_day_constrains(constraint_model, works_shift_on_day)
#
#         new_emps_first_shift = generate_new_employees_on_shift(employees, shifts, shift_combinations, ShiftTypesEnum.EVENING, day)
#         new_emps_second_shift = generate_new_employees_on_shift(employees, shifts, shift_combinations, ShiftTypesEnum.CLOSING, day)
#
#         add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, constraint_model, new_emps_first_shift, new_emps_second_shift, day)
