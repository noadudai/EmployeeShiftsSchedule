import datetime
import random
from uuid import uuid4

from ortools.sat.python import cp_model

from src.constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_at_most_one_shift_per_employee_in_the_same_day_constraint, \
    add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint
from src.models.employees.employee import Employee
from src.models.employees.employee_position_enum import EmployeePositionEnum
from src.models.employees.employee_priority_enum import EmployeePriorityEnum
from src.models import EmployeeStatusEnum
from src.models.shifts.shift import Shift
from src.models.shifts import ShiftCombinationsKey
from src.models.shifts import ShiftTypesEnum


def test_no_optimal_solution_when_the_closing_shift_and_the_next_shift_are_too_close_to_each_other():
    minimum_time_between_shifts = datetime.timedelta(hours=9)
    end_closing_shift_time = datetime.datetime(2023, 12, 12, 2, 0)
    start_closing_shift_time = datetime.datetime(2023, 12, 11, random.randint(13, 23))

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    closing_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=start_closing_shift_time , end_time=end_closing_shift_time)

    # the forbidden shift starts 3 hour before the minimum time between the shifts passed
    start_forbidden_shift_time = closing_shift.end_time + (minimum_time_between_shifts - datetime.timedelta(hours=3))
    shift_too_close_to_closing_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=start_forbidden_shift_time, end_time=start_forbidden_shift_time + datetime.timedelta(random.random()))

    shifts = [closing_shift, shift_too_close_to_closing_shift]
    employees = [test_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    afternoon_start_time = datetime.time(12, 30)
    add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts, afternoon_start_time)

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
    afternoon_start_time = datetime.time(12, 30)
    add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts, afternoon_start_time)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)


def test_all_the_employees_who_worked_in_the_afternoon_are_not_working_in_the_morning_of_the_day_after():
    minimum_time_between_shifts = datetime.timedelta(hours=9)
    shift_duration = datetime.timedelta(minutes=random.random())

    # up to 29 because there are months that do not go up to 31 or even 30 days.
    morning_shift_start_time = datetime.datetime(2024, random.randint(1, 12), random.randint(1, 29), 7, 30)
    afternoon_shift_end_time = morning_shift_start_time - (minimum_time_between_shifts/2)
    afternoon_shift_start_time = afternoon_shift_end_time - shift_duration

    afternoon_shift = Shift(shift_id="afternoon_shift", shift_type=ShiftTypesEnum.EVENING, start_time=afternoon_shift_start_time, end_time=afternoon_shift_end_time)
    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=morning_shift_start_time, end_time=morning_shift_start_time + shift_duration)

    afternoon_employee = Employee(name="afternoon_employee", employee_id="afternoon_employee")
    morning_employee = Employee(name="morning_employee", employee_id="morning_employee")

    shifts = [afternoon_shift, morning_shift]
    employees = [afternoon_employee, morning_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    afternoon_employee_working_evening_key = ShiftCombinationsKey(afternoon_employee.employee_id, afternoon_shift.shift_id)
    morning_employee_working_morning_key = ShiftCombinationsKey(morning_employee.employee_id, morning_shift.shift_id)

    # manually assigning the afternoon employee to the evening shift
    model.Add(all_shifts[afternoon_employee_working_evening_key] == 1)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)
    evening_shifts_start_time = datetime.time(16)
    add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts, evening_shifts_start_time)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    assert solver.Value(all_shifts[morning_employee_working_morning_key]) == True
