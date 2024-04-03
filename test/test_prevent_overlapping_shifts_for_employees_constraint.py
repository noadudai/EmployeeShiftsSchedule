import datetime
import random
from uuid import uuid4

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_employees_can_work_non_overlapping_shifts():
    """
    |shift1     | |shift2       |
    """
    test_shift_start_time = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=test_shift_start_time, end_time=test_shift_start_time + shift_duration)
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift.end_time + shift_duration, end_time=test_shift.end_time + (shift_duration * 2))

    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    employees = [test_employee]
    shifts = [test_shift, test_shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    expected_employee_working = True

    test_employee_working_test_shift2_key = ShiftCombinationsKey(test_employee.employee_id, test_shift2.shift_id)
    test_employee_working_test_shift2 = solver.Value(all_shifts[test_employee_working_test_shift2_key]) == expected_employee_working

    test_employee_working_test_shift_key = ShiftCombinationsKey(test_employee.employee_id, test_shift.shift_id)
    test_employee_working_test_shift = solver.Value(all_shifts[test_employee_working_test_shift_key]) == expected_employee_working

    assert test_employee_working_test_shift2 and test_employee_working_test_shift


def test_employees_can_not_work_overlapping_shifts():
    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=shift_a_start_time, end_time=shift_a.end_time + shift_duration)

    model = cp_model.CpModel()
    employees = [test_employee]
    shifts = [shift_a, shift_b]

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)


def test_a_shift_that_starts_when_a_different_shift_ends_does_not_overlaps_with_each_other():
    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    main_shift_start_time = datetime.datetime(2024, 1, 11, 9, 0)
    shift_duration = datetime.timedelta(minutes=30)
    main_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=main_shift_start_time + shift_duration)
    shift_bigger_then_main_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=main_shift.end_time, end_time=main_shift.end_time + (shift_duration / 2))

    model = cp_model.CpModel()
    employees = [test_employee]
    shifts = [main_shift, shift_bigger_then_main_shift]

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    # The employee can work the 2 shifts because the shifts does not overlap
    assert (solver.Value(all_shifts[ShiftCombinationsKey(test_employee.employee_id, main_shift.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(test_employee.employee_id, shift_bigger_then_main_shift.shift_id)]) == True)