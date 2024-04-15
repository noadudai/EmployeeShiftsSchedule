import datetime
import random
from uuid import uuid4

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_at_most_one_shift_per_employee_in_the_same_day_constraint, \
    add_minimum_time_between_afternoon_shifts_and_next_shift_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
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
    add_minimum_time_between_afternoon_shifts_and_next_shift_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts)

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
    add_minimum_time_between_afternoon_shifts_and_next_shift_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)


def test_all_the_employees_who_worked_in_the_afternoon_are_not_working_in_the_morning_of_the_day_after():
    """
            THURSDAY
                16:00 - 02:00
                |      |
                    19:30 - 03:00
                    |       |
                        21:30 - 04:00
                        |       |
            FRIDAY
    07:30 - random
    |       |
    """

    thursday_evening_shift = Shift(shift_id="evening_shift", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 11, 16, 0), end_time=datetime.datetime(2024, 4, 12, 2))
    thursday_evening_backup_shift = Shift(shift_id="evening_backup_shift", shift_type=ShiftTypesEnum.THURSDAY_BACKUP, start_time=datetime.datetime(2024, 4, 11, 19, 30), end_time=datetime.datetime(2024, 4, 12, 3))
    thursday_closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 11, 21, 30), end_time=datetime.datetime(2024, 4, 12, 4))
    friday_morning = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 4, 12, 7, 30), end_time=datetime.datetime(2024, 4, 12, 7, 30) + datetime.timedelta(minutes=random.random()))

    thursday_evening_employee = Employee(name="thursday_evening_employee", employee_id="thursday_evening_employee")
    thursday_backup_employee = Employee(name="thursday_backup_employee", employee_id="thursday_backup_employee")
    thursday_closing_employee = Employee(name="thursday_closing_employee", employee_id="thursday_closing_employee")

    friday_morning_employee = Employee(name="friday_morning_employee", employee_id="friday_morning_employee")

    shifts = [thursday_evening_shift, thursday_evening_backup_shift, thursday_closing_shift, friday_morning]
    employees = [thursday_evening_employee, thursday_backup_employee, thursday_closing_employee, friday_morning_employee]

    minimum_time_between_shifts = datetime.timedelta(hours=9)

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    thursday_evening_employee_working_evening_key = ShiftCombinationsKey(thursday_evening_employee.employee_id, thursday_evening_shift.shift_id)
    thursday_backup_employee_works_backup_key = ShiftCombinationsKey(thursday_backup_employee.employee_id, thursday_evening_backup_shift.shift_id)
    thursday_closing_employee_works_backup_key = ShiftCombinationsKey(thursday_closing_employee.employee_id, thursday_closing_shift.shift_id)
    friday_morning_employee_works_friday_morning_key = ShiftCombinationsKey(friday_morning_employee.employee_id, friday_morning.shift_id)

    model.Add(all_shifts[thursday_evening_employee_working_evening_key] == 1)
    model.Add(all_shifts[thursday_backup_employee_works_backup_key] == 1)
    model.Add(all_shifts[thursday_closing_employee_works_backup_key] == 1)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)
    add_minimum_time_between_afternoon_shifts_and_next_shift_constraint(shifts, employees, model, all_shifts, minimum_time_between_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    assert solver.Value(all_shifts[friday_morning_employee_works_friday_morning_key]) == True
