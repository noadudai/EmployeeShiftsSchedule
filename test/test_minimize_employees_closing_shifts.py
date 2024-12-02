import datetime
import random
import uuid

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_minimize_given_closing_shifts_for_employees_constraint
from models.employees.employee import Employee
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_number_of_closing_shift_is_evenly_divided_between_the_emps():
    shift_start_time_for_test = datetime.datetime.now()
    shift_duration = datetime.timedelta(hours=random.random())
    shifts: list[Shift] = []

    for i in range(8):
        shifts.append(Shift(shift_id=uuid.uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=shift_start_time_for_test + datetime.timedelta(days=i), end_time=shift_start_time_for_test + datetime.timedelta(days=i) + shift_duration))

    emp1 = Employee(name="emp1", employee_id="emp1")
    emp2 = Employee(name="emp2", employee_id="emp2")

    employees: list[Employee] = [emp1, emp2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_minimize_given_closing_shifts_for_employees_constraint(employees, shifts, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    for emp in employees:
        num_shifts = 0
        for sift in shifts:
            if solver.Value(all_shifts[ShiftCombinationsKey(emp.employee_id, sift.shift_id)]):
                num_shifts += 1

        assert (num_shifts == 4)


def test_only_one_emp_gets_extra_closing_shift():
    shift_start_time_for_test = datetime.datetime.now()
    shift_duration = datetime.timedelta(hours=random.random())
    sb_shifts: list[Shift] = []

    emp1 = Employee(name="emp1", employee_id="emp1")
    emp2 = Employee(name="emp2", employee_id="emp2")

    employees: list[Employee] = [emp1, emp2]

    for i in range(len(employees) + 1):
        sb_shifts.append(Shift(shift_id=uuid.uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=shift_start_time_for_test + datetime.timedelta(days=i), end_time=shift_start_time_for_test + datetime.timedelta(days=i) + shift_duration))

    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, sb_shifts, model)
    add_exactly_one_employee_per_shift_constraint(sb_shifts, employees, model, all_shifts)
    add_minimize_given_closing_shifts_for_employees_constraint(employees, sb_shifts, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    emps_number_of_shifts = {}
    for emp in employees:
        num_shifts = 0
        for sift in sb_shifts:
            if solver.Value(all_shifts[ShiftCombinationsKey(emp.employee_id, sift.shift_id)]):
                num_shifts += 1
        emps_number_of_shifts[emp.employee_id] = num_shifts

    assert (max(emps_number_of_shifts.values()) == 2)