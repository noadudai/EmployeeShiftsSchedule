import datetime
import random

import pytest
from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint
from models.employees.employee import Employee
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_no_schedule_when_an_employee_cannot_work_a_shift_because_he_is_not_trained_to_do_that_shift():
    employee_who_cannot_close = Employee(name="employee_who_cannot_close", shifts_trained_to_do=[ShiftTypesEnum.MORNING])

    closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    employees = [employee_who_cannot_close]

    shifts = [closing_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)


def test_an_employee_who_is_not_trained_to_work_a_shift_is_not_working_that_shift():
    employee_who_cannot_work_morning = Employee(name="employee_who_cannot_work_morning", employee_id="employee_who_cannot_work_morning", shifts_trained_to_do=[ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP])
    employee_who_can_work_morning = Employee(name="employee_who_can_work_morning", employee_id="employee_who_can_work_morning", shifts_trained_to_do=[ShiftTypesEnum.MORNING])

    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))
    morning_shift2 = Shift(shift_id="morning_shift2", shift_type=ShiftTypesEnum.MORNING, start_time=morning_shift.end_time, end_time=morning_shift.end_time + datetime.timedelta(minutes=random.random()))

    employees = [employee_who_cannot_work_morning, employee_who_can_work_morning]

    shifts = [morning_shift, morning_shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    employee_who_can_work_morning_working_morning_shift_key = all_shifts[ShiftCombinationsKey(employee_who_can_work_morning.employee_id, morning_shift.shift_id)]
    assert (solver.Value(employee_who_can_work_morning_working_morning_shift_key) == True)

    employee_who_can_work_morning_working_morning_shift2_key = all_shifts[ShiftCombinationsKey(employee_who_can_work_morning.employee_id, morning_shift2.shift_id)]
    assert (solver.Value(employee_who_can_work_morning_working_morning_shift2_key) == True)

    employee_who_cannot_work_morning_working_morning_shift_key = all_shifts[ShiftCombinationsKey(employee_who_cannot_work_morning.employee_id, morning_shift.shift_id)]
    assert (solver.Value(employee_who_cannot_work_morning_working_morning_shift_key) == False)


def test_no_schedule_when_there_are_2_emps_and_one_of_them_is_not_trained_to_do_any_of_the_shifts():
    employee_who_cannot_work_morning = Employee(name="employee_who_cannot_work_morning", employee_id="employee_who_cannot_work_morning", shifts_trained_to_do=[ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP])
    employee_who_can_work_morning = Employee(name="employee_who_can_work_morning", employee_id="employee_who_can_work_morning", shifts_trained_to_do=[ShiftTypesEnum.MORNING])

    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))
    morning_shift2 = Shift(shift_id="morning_shift2", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    employees = [employee_who_cannot_work_morning, employee_who_can_work_morning]

    shifts = [morning_shift, morning_shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)
