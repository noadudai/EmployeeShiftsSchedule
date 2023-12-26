import datetime
from uuid import uuid4

import pytest
from ortools.sat.python import cp_model


from constraints_file import *
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


# A function to create an employee for testing, so that the uuid will be generated for the 'program user'
def create_employee(name: str, priority: EmployeePriorityEnum, status: EmployeeStatusEnum) -> Employee:
    return Employee(name, priority, status, employee_id=uuid4())


# a Test to check that there is an optimal solution and that there is at least one employee that is working that
# shift and that the other employee does not.
# Expected solution is Optimal and that the first employee is assigned to the shift.
def test_add_exactly_one_employee_per_shift_constraint():
    test_employee = create_employee("test", priority=EmployeePriorityEnum.HIGHEST, status=EmployeeStatusEnum.senior_employee)
    test_employee2 = create_employee("test2", priority=EmployeePriorityEnum.HIGHEST, status=EmployeeStatusEnum.senior_employee)

    employees = [test_employee, test_employee2]

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_exactly_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    first_employee_assignment = shifts[FrozenShiftCombinationsKey(test_employee.employee_id, test_shift.shift_id)]
    expected_first_employee_working = True
    assert (solver.Value(first_employee_assignment) == expected_first_employee_working)

    second_employee_assignment = shifts[FrozenShiftCombinationsKey(test_employee2.employee_id, test_shift.shift_id)]
    expected_second_employee_working = False
    assert (solver.Value(second_employee_assignment) == expected_second_employee_working)


# A Test to check if there is an optimal solution with 0 employees, while satisfying the
# 'add_exactly_one_employee_per_shift_constraint' constraint.
# Expected result is not an Optimal solution because there is no employee to assign to the shift.
def test_add_exactly_one_employee_per_shift_constraint_with_no_employees():
    employees = []

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_exactly_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)


# A Test to check if there is an optimal solution with 2 employees and 3 shifts.
# Expected result is an Optimal solution because there is a solution where no employee is assigned to shifts.
def test_add_at_most_one_shift_per_employee_in_the_same_day_constraint_without_add_exactly_one_employee_per_shift_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))
    test_shift3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2023, 12, 11, 17, 30), end_time=datetime.datetime(2023, 12, 12, 2, 0))

    shifts = [test_shift1, test_shift2, test_shift3]
    employees = [test_employee, test_employee2]
    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # there is a solution where employees are not assigned to shifts, which is considered an optimal solution.
    assert (status == cp_model.OPTIMAL)
    expected_employee_working = False

    for shift in shifts:
        for employee in employees:
            key = FrozenShiftCombinationsKey(employee.employee_id, shift.shift_id)
            working_assignment = all_shifts[key]
            # the employee does not work this shift
            assert (solver.Value(working_assignment) == expected_employee_working)


# A Test to check if there is an optimal solution with 2 employees and 3 shifts. With at least one employee that is
# working each shift. There is no optimal solution because there are fewer employees than the shift in the same day.
def test_add_at_most_one_shift_per_employee_in_the_same_day_constraint_with_at_least_one_employee_in_a_shift_with_3_shifts_2_employees():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))
    test_shift3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2023, 12, 11, 17, 30), end_time=datetime.datetime(2023, 12, 12, 2, 0))

    shifts = [test_shift1, test_shift2, test_shift3]
    employees = [test_employee, test_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    # When adding the constraint "add_one_employee_per_shift_constraint", it also ensures that there is exactly one
    # employee in each shift, causing "add_at_most_one_shift_in_the_same_day_constraint" to fail; because the solver
    # needs to assign exactly one employee in each shift, and cannot assign an employee to at most 1 shift a day.
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status != cp_model.OPTIMAL)


# A test that checks if the constraint 'add_at_most_one_shift_in_the_same_day_constraint' ensures that an employee does
# not work more than 1 shift a day (at most one shift a day).
def test_add_at_most_one_shift_per_employee_in_the_same_day_constraint_with_at_least_one_employee_in_a_shift():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee,  employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))

    shifts = [test_shift1, test_shift2]
    employees = [test_employee, test_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    # When adding the constraint "add_one_employee_per_shift_constraint", it also ensures that there is exactly one
    # employee in each shift. With 2 employees and 2 shifts that starts at the same day, there is an Optimal solution.
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    expected_employee_working = True

    first_emp_first_shift_key = FrozenShiftCombinationsKey(test_employee.employee_id, test_shift1.shift_id)
    first_emp_second_shift_key = FrozenShiftCombinationsKey(test_employee.employee_id, test_shift2.shift_id)
    second_emp_first_shift_key = FrozenShiftCombinationsKey(test_employee2.employee_id, test_shift1.shift_id)
    second_emp_second_shift_key = FrozenShiftCombinationsKey(test_employee2.employee_id, test_shift2.shift_id)

    if solver.Value(all_shifts[first_emp_first_shift_key]) == expected_employee_working:
        assert (solver.Value(all_shifts[first_emp_second_shift_key]) != expected_employee_working)
    elif solver.Value(all_shifts[second_emp_first_shift_key]) == expected_employee_working:
        assert (solver.Value(all_shifts[second_emp_second_shift_key]) != expected_employee_working)
