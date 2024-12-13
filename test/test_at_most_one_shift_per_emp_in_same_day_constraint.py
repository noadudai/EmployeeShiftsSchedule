import datetime
import random
from uuid import uuid4

from ortools.sat.python import cp_model

from src.constraints_file import generate_shift_employee_combinations, \
    add_at_most_one_shift_per_employee_in_the_same_day_constraint, add_exactly_one_employee_per_shift_constraint
from src.models.employees.employee import Employee
from src.models.employees.employee_position_enum import EmployeePositionEnum
from src.models.employees.employee_priority_enum import EmployeePriorityEnum
from src.models import EmployeeStatusEnum
from src.models.shifts.shift import Shift
from src.models.shifts import ShiftCombinationsKey
from src.models.shifts import ShiftTypesEnum


def test_every_shift_has_an_assigned_employee_and_every_employee_has_at_most_one_shift_in_the_same_day():
    shift_start_time_for_test = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)
    employees = [test_employee]

    shifts: list[Shift] = []
    for i in range(len(employees) + 1):
        shifts.append(Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=shift_start_time_for_test + datetime.timedelta(days=i), end_time=shift_start_time_for_test + shift_duration))

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
    for shift in shifts:
        key = ShiftCombinationsKey(test_employee.employee_id, shift.shift_id)
        emp_working_shift = solver.Value(all_shifts[key]) == expected_employee_working

        assert emp_working_shift


def test_verify_no_optimal_solution_when_there_are_more_shifts_then_employees():
    shift_start_time_for_test = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    employees = [test_employee, test_employee2]

    shifts: list[Shift] = []

    for _ in range(len(employees) + 1):
        shifts.append(Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=shift_start_time_for_test, end_time=shift_start_time_for_test + shift_duration))

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