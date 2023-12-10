import itertools

import pytest
from ortools.sat.python import cp_model

from constraints import generate_new_employees_on_shift, generate_shift_employee_combinations
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift_type import ShiftType
from models.shifts.shifts_types_enum import ShiftTypesEnum
from smaller_constraints import *


def test_add_at_most_one_employee_per_shift_constrain():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    employees = [test_employee, test_employee2]

    start_time_of_shift = datetime.time(9, 30)
    start_date_of_shift = datetime.date(2023, 11, 12)
    end_time_of_shift = datetime.time(16, 0)
    end_date_of_shift = datetime.date(2023, 11, 12)

    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, start_time_of_shift, end_time_of_shift), start_date_of_shift, end_date_of_shift)

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift], constraint_model)

    for shift in [test_shift]:
        employees_on_shift = [shift_combinations[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)] for employee in employees]
        add_at_most_one_employee_per_shift_constrain(constraint_model, employees_on_shift)

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
    # the employee does not work this shift
    assert (solver.Value(second_employee_assignment) == expected_employee_working)


def test_add_at_most_one_employee_per_shift_a_day_with_no_employees_constrains():
    employees = []

    start_time_of_shift = datetime.time(9, 30)
    start_date_of_shift = datetime.date(2023, 11, 12)
    end_time_of_shift = datetime.time(16, 0)
    end_date_of_shift = datetime.date(2023, 11, 12)

    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, start_time_of_shift, end_time_of_shift), start_date_of_shift, end_date_of_shift)

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations(employees, [test_shift], constraint_model)

    for shift in [test_shift]:
        employees_on_shift = [shift_combinations[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)] for employee in employees]
        add_at_most_one_employee_per_shift_a_day_constrains(constraint_model, employees_on_shift)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    # there is a solution where employees are not assigned to shifts, which is considered an optimal solution.
    assert (status == cp_model.OPTIMAL)
