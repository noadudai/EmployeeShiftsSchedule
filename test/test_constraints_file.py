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
def test_add_at_least_one_employee_per_shift_constraint():
    test_employee = create_employee("test", priority=EmployeePriorityEnum.HIGHEST, status=EmployeeStatusEnum.senior_employee)
    test_employee2 = create_employee("test2", priority=EmployeePriorityEnum.HIGHEST, status=EmployeeStatusEnum.senior_employee)

    employees = [test_employee, test_employee2]

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_at_least_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

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
# 'add_at_least_one_employee_per_shift_constraint' constraint.
# Expected result is not an Optimal solution because there is no employee to assign to the shift.
def test_add_at_least_one_employee_per_shift_constraint_with_no_employees():
    employees = []

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_at_least_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)
