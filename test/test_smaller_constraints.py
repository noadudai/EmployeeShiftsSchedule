import itertools

import pytest
from ortools.sat.python import cp_model

from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift_type import ShiftType
from models.shifts.shifts_types_enum import ShiftTypesEnum
from smaller_constraints import *


def test_add_at_most_one_shift_for_employee_in_a_day_constrain():
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

    employees_on_shift = [shift_combinations[FrozenShiftCombinationKey(employee.id, test_shift.start_date_of_shift, test_shift.end_date_of_shift, test_shift.shift_type.name_of_shift)] for employee in employees]
    # Without "add_at_least_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_at_least_one_employee_per_shift_constraint(constraint_model, employees_on_shift)

    days_in_the_given_shift_list = list(set(shift.start_date_of_shift for shift in [test_shift]))
    for day in days_in_the_given_shift_list:
        for shift in [test_shift]:
            start_date = shift.start_date_of_shift

            if start_date == day:
                works_shifts_on_day = [shift_combinations[FrozenShiftCombinationKey(employee.id, shift.start_date_of_shift, shift.end_date_of_shift, shift.shift_type.name_of_shift)] for employee in employees]
                add_at_most_one_shift_for_employee_in_a_day_constrain(constraint_model, works_shifts_on_day)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    start_shift = test_shift.start_date_of_shift
    end_shift = test_shift.end_date_of_shift
    shift_type = test_shift.shift_type.name_of_shift

    assert (status == cp_model.OPTIMAL)

    # One of the employees does not work in the same shift as the other employee
    expected_employee_working = False

    if solver.Value(shift_combinations[FrozenShiftCombinationKey(test_employee.id, start_shift, end_shift, shift_type)]):
        is_employee_working_value = solver.Value(shift_combinations[FrozenShiftCombinationKey(test_employee2.id, start_shift, end_shift, shift_type)])
        assert (is_employee_working_value == expected_employee_working)
    elif solver.Value(shift_combinations[FrozenShiftCombinationKey(test_employee2.id, start_shift, end_shift, shift_type)]):
        is_employee_working_value = solver.Value(shift_combinations[FrozenShiftCombinationKey(test_employee.id, start_shift, end_shift, shift_type)])
        assert (is_employee_working_value == expected_employee_working)


# Without "add_at_least_one_employee_per_shift_constraint", the expected solution with no employees is: Optimal.
# Because there is a solution where employees are not assigned to shifts, which is considered an optimal solution.
def test_add_at_most_one_shift_for_employee_in_a_day_with_no_employees_constrains():
    employees = []

    start_time_of_shift = datetime.time(9, 30)
    start_date_of_shift = datetime.date(2023, 11, 12)
    end_time_of_shift = datetime.time(16, 0)
    end_date_of_shift = datetime.date(2023, 11, 12)

    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, start_time_of_shift, end_time_of_shift), start_date_of_shift, end_date_of_shift)

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations(employees, [test_shift], constraint_model)

    days_in_the_given_shift_list = list(set(shift.start_date_of_shift for shift in [test_shift]))
    for day in days_in_the_given_shift_list:
        for shift in [test_shift]:
            start_date = shift.start_date_of_shift

            if start_date == day:
                works_shifts_on_day = [shift_combinations[FrozenShiftCombinationKey(employee.id, shift.start_date_of_shift, shift.end_date_of_shift, shift.shift_type.name_of_shift)] for employee in employees]
                add_at_most_one_shift_for_employee_in_a_day_constrain(constraint_model, works_shifts_on_day)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    assert (status == cp_model.OPTIMAL)


# With "add_at_least_one_employee_per_shift_constraint", the expected solution with no employees is not Optimal.
# Because the model needs to assign at least one employee for each shift and there are no employees to assign to shifts.
def test_add_at_most_one_and_at_least_one_employee_per_shift_a_day_with_no_employees_constrains():
    employees = []

    start_time_of_shift = datetime.time(9, 30)
    start_date_of_shift = datetime.date(2023, 11, 12)
    end_time_of_shift = datetime.time(16, 0)
    end_date_of_shift = datetime.date(2023, 11, 12)

    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, start_time_of_shift, end_time_of_shift), start_date_of_shift, end_date_of_shift)

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations(employees, [test_shift], constraint_model)

    employees_on_shift = [shift_combinations[FrozenShiftCombinationKey(employee.id, test_shift.start_date_of_shift, test_shift.end_date_of_shift, test_shift.shift_type.name_of_shift)] for employee in employees]
    # Without "add_at_least_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_at_least_one_employee_per_shift_constraint(constraint_model, employees_on_shift)

    days_in_the_given_shift_list = list(set(shift.start_date_of_shift for shift in [test_shift]))
    for day in days_in_the_given_shift_list:
        for shift in [test_shift]:
            start_date = shift.start_date_of_shift

            if start_date == day:
                works_shifts_on_day = [shift_combinations[FrozenShiftCombinationKey(employee.id, shift.start_date_of_shift, shift.end_date_of_shift, shift.shift_type.name_of_shift)] for employee in employees]
                add_at_most_one_shift_for_employee_in_a_day_constrain(constraint_model, works_shifts_on_day)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    assert (status != cp_model.OPTIMAL)
