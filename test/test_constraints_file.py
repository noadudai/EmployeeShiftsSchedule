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


def test_every_shift_has_an_assigned_employee():
    test_employee = create_employee("test", priority=EmployeePriorityEnum.HIGHEST, status=EmployeeStatusEnum.senior_employee)
    test_employee2 = create_employee("test2", priority=EmployeePriorityEnum.HIGHEST, status=EmployeeStatusEnum.senior_employee)

    employees = [test_employee, test_employee2]

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_exactly_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    first_employee_assignment = shifts[ShiftCombinationsKey(test_employee.employee_id, test_shift.shift_id)]
    expected_first_employee_working = True
    assert (solver.Value(first_employee_assignment) == expected_first_employee_working)

    second_employee_assignment = shifts[ShiftCombinationsKey(test_employee2.employee_id, test_shift.shift_id)]
    expected_second_employee_working = False
    assert (solver.Value(second_employee_assignment) == expected_second_employee_working)


def test_verify_no_optimal_solution_when_there_are_no_employees_to_assign_to_shifts():
    employees = []

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations(employees, [test_shift], model)
    add_exactly_one_employee_per_shift_constraint([test_shift], employees, model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)


def test_every_shift_has_an_assigned_employee_and_every_employee_has_at_most_one_shift_in_the_same_day():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee,  employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))

    shifts = [test_shift1, test_shift2]
    employees = [test_employee, test_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    # When adding the constraint "add_one_employee_per_shift_constraint", it also ensures that there is exactly one
    # employee in each shift. With 2 employees and 2 shifts that starts at the same day, there is an Optimal solution.
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    first_emp_first_shift_key = ShiftCombinationsKey(test_employee.employee_id, test_shift1.shift_id)
    first_emp_second_shift_key = ShiftCombinationsKey(test_employee.employee_id, test_shift2.shift_id)
    second_emp_first_shift_key = ShiftCombinationsKey(test_employee2.employee_id, test_shift1.shift_id)
    second_emp_second_shift_key = ShiftCombinationsKey(test_employee2.employee_id, test_shift2.shift_id)

    expected_employee_working = True
    expected_employee_not_working = False

    emp1_working_shift1 = solver.Value(all_shifts[first_emp_first_shift_key]) == expected_employee_working
    emp1_working_shift2 = solver.Value(all_shifts[first_emp_second_shift_key]) == expected_employee_not_working

    emp2_working_shift1 = solver.Value(all_shifts[second_emp_first_shift_key]) == expected_employee_working
    emp_working_shift2 = solver.Value(all_shifts[second_emp_second_shift_key]) == expected_employee_not_working

    if emp1_working_shift1:
        assert emp1_working_shift2
    elif emp2_working_shift1:
        assert emp_working_shift2


def test_verify_no_optimal_solution_when_there_are_more_shifts_then_employees():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))
    test_shift3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2023, 12, 11, 17, 30), end_time=datetime.datetime(2023, 12, 12, 2, 0))

    shifts = [test_shift1, test_shift2, test_shift3]
    employees = [test_employee, test_employee2]

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


def test_verify_no_optimal_solution_when_there_are_more_shifts_then_max_working_shifts_for_one_employee():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))
    test_shift3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2023, 12, 11, 17, 30), end_time=datetime.datetime(2023, 12, 12, 2, 0))

    shifts = [test_shift1, test_shift2, test_shift3]
    employees = [test_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    max_working_days = 2
    add_limit_employees_working_days_constraint(shifts, employees, model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # Expected no optimal solution because there are more shifts than max_working_days, and there is only one employee.
    assert (status != cp_model.OPTIMAL)


def test_every_employee_does_not_work_more_then_max_working_days():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 12, 16, 0), end_time=datetime.datetime(2023, 12, 12, 22, 0))

    shifts = [test_shift1, test_shift2]
    employees = [test_employee, test_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    max_working_days = 1
    add_limit_employees_working_days_constraint(shifts, employees, model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    first_emp_first_shift_key = ShiftCombinationsKey(test_employee.employee_id, test_shift1.shift_id)
    first_emp_second_shift_key = ShiftCombinationsKey(test_employee.employee_id, test_shift2.shift_id)
    second_emp_first_shift_key = ShiftCombinationsKey(test_employee2.employee_id, test_shift1.shift_id)
    second_emp_second_shift_key = ShiftCombinationsKey(test_employee2.employee_id, test_shift2.shift_id)

    expected_employee_working = True
    expected_employee_not_working = False

    emp1_working_shift1 = solver.Value(all_shifts[first_emp_first_shift_key]) == expected_employee_working
    emp1_working_shift2 = solver.Value(all_shifts[first_emp_second_shift_key]) == expected_employee_not_working

    emp2_working_shift1 = solver.Value(all_shifts[second_emp_first_shift_key]) == expected_employee_working
    emp_working_shift2 = solver.Value(all_shifts[second_emp_second_shift_key]) == expected_employee_not_working

    if emp1_working_shift1:
        assert emp1_working_shift2
    elif emp2_working_shift1:
        assert emp_working_shift2


def test_verify_working_days_for_employee_does_not_exceed_the_max_working_days():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    test_employee3 = Employee("test3", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())

    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))
    test_shift3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 12, 16, 0), end_time=datetime.datetime(2023, 12, 12, 22, 0))
    test_shift4 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2023, 12, 12, 16, 0), end_time=datetime.datetime(2023, 12, 13, 22, 0))
    test_shift5 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 13, 16, 0), end_time=datetime.datetime(2023, 12, 13, 22, 0))

    shifts = [test_shift1, test_shift2, test_shift3, test_shift4, test_shift5]
    employees = [test_employee, test_employee2, test_employee3]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    max_working_days = 2
    add_limit_employees_working_days_constraint(shifts, employees, model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    employees_shifts: dict[Employee.employee_id, int] = {}

    for employee in employees:
        employees_shifts[employee.employee_id] = 0
        for shift in shifts:
            key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
            employee_assignment = solver.Value(all_shifts[key])

            if employee_assignment:
                employees_shifts[employee.employee_id] += 1

    assert (max(employees_shifts.values()) <= max_working_days)


def test_no_optimal_solution_when_the_closing_shift_and_the_next_shift_are_too_close_to_each_other():
    minimum_time_between_shifts = datetime.timedelta(hours=9)
    shift_duration = datetime.timedelta(hours=8)
    start_closing_shift_time = datetime.datetime(2023, 12, 12, 18, 0)

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())

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

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())

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
