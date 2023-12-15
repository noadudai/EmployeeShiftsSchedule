import datetime
import pytest
from ortools.sat.python import cp_model


from constraints import *
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_add_at_least_one_employee_per_shift_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee)

    employees = [test_employee, test_employee2]

    test_shift = (Shift(ShiftTypesEnum.MORNING, datetime.datetime(2023, 12, 11, 9, 30), datetime.datetime(2023, 12, 11, 16, 0)))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_at_least_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    second_employee_assignment = shifts[FrozenShiftCombinationsKey(test_employee2.id, test_shift.shift_id)]
    expected_employee_working = False

    assert (solver.Value(second_employee_assignment) == expected_employee_working)


# Expected result is not an Optimal solution because there is no employee to assign to the shift.
def test_add_at_least_one_employee_per_shift_constraint_with_no_employees():
    employees = []

    test_shift = (Shift(ShiftTypesEnum.MORNING, datetime.datetime(2023, 12, 11, 9, 30), datetime.datetime(2023, 12, 11, 16, 0)))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_at_least_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)
