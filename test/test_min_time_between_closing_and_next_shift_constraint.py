import datetime
import random
from uuid import uuid4

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_at_most_one_shift_per_employee_in_the_same_day_constraint, \
    add_minimum_time_between_closing_shift_and_next_shift_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_no_optimal_solution_when_the_closing_shift_and_the_next_shift_are_too_close_to_each_other():
    minimum_time_between_shifts = datetime.timedelta(hours=9)
    shift_duration = datetime.timedelta(hours=random.random())
    start_closing_shift_time = datetime.datetime(2023, 12, 12, 18, 0)

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    closing_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=start_closing_shift_time, end_time=start_closing_shift_time + shift_duration)

    # the forbidden shift starts 1 hour before the minimum time between the shifts passed
    start_forbidden_shift_time = closing_shift.end_time + minimum_time_between_shifts - datetime.timedelta(hours=1)
    shift_too_close_to_closing_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=start_forbidden_shift_time, end_time=start_forbidden_shift_time + shift_duration)

    shifts = [closing_shift, shift_too_close_to_closing_shift]
    employees = [test_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)
    add_minimum_time_between_closing_shift_and_next_shift_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status != cp_model.OPTIMAL)


def test_every_employee_that_worked_closing_shift_does_not_work_the_next_shifts_that_are_too_close_to_the_closing_shift():
    minimum_time_between_shifts = datetime.timedelta(hours=9)
    shift_duration = datetime.timedelta(hours=8)
    start_closing_shift_time = datetime.datetime(2023, 12, 12, 18, 0)

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    closing_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=start_closing_shift_time, end_time=start_closing_shift_time + shift_duration)

    # the forbidden shift starts 1 hour after the minimum time between the shifts passed
    start_available_shift_time = closing_shift.end_time + minimum_time_between_shifts + datetime.timedelta(hours=1)
    available_shift_after_closing_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=start_available_shift_time, end_time=start_available_shift_time + shift_duration)

    shifts = [closing_shift, available_shift_after_closing_shift]
    employees = [test_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)
    add_minimum_time_between_closing_shift_and_next_shift_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)