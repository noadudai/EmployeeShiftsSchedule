import datetime
import random
from uuid import uuid4

from ortools.sat.python import cp_model

from src.constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_limit_employees_working_days_constraint, add_at_most_one_shift_per_employee_in_the_same_day_constraint
from src.models.employees.employee import Employee
from src.models.employees.employee_position_enum import EmployeePositionEnum
from src.models.employees.employee_priority_enum import EmployeePriorityEnum
from src.models import EmployeeStatusEnum
from src.models.shifts.shift import Shift
from src.models.shifts import ShiftCombinationsKey
from src.models.shifts import ShiftTypesEnum


def test_verify_no_optimal_solution_when_there_are_more_shifts_then_max_working_shifts_for_one_employee():
    shift_start_time_for_test = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

    employees = [test_employee]
    shifts: list[Shift] = []

    for _ in range(len(employees) + 1):
        shifts.append(Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=shift_start_time_for_test,
                            end_time=shift_start_time_for_test + shift_duration))

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    max_working_days = 1
    add_limit_employees_working_days_constraint(shifts, employees, model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # Expected no optimal solution because there are more shifts than max_working_days, and there is only one employee.
    assert (status != cp_model.OPTIMAL)


def test_verify_working_days_for_employee_does_not_exceed_the_max_working_days():
    shift_start_time_for_test = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    max_working_days = 2
    employees: list[Employee] = []
    shifts: list[Shift] = []

    for _ in range(0, 2):
        employees.append(Employee(f"{_}", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer))

    for i in range(len(employees) + 1):
        shifts.append(Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=shift_start_time_for_test + datetime.timedelta(days=i), end_time=shift_start_time_for_test + shift_duration))

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)
    add_limit_employees_working_days_constraint(shifts, employees, model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    employees_schedule: dict[Employee.employee_id, int] = {}
    for employee in employees:
        employees_schedule[employee.employee_id] = 0
        for shift in shifts:
            key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
            employee_assignment = solver.Value(all_shifts[key])
            if employee_assignment:
                employees_schedule[employee.employee_id] += 1

    assert (max(employees_schedule.values()) <= max_working_days)