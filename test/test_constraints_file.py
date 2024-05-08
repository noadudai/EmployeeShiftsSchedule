import datetime
import random
from uuid import uuid4
import pytest
from ortools.sat.python import cp_model
from .var_array_solution_printer import VarArraySolutionPrinter

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_at_most_one_shift_per_employee_in_the_same_day_constraint, add_limit_employees_working_days_constraint, \
    add_minimum_time_between_closing_shift_and_next_shift_constraint, \
    add_prevent_new_employees_from_working_parallel_shifts_together, \
    add_prevent_overlapping_shifts_for_employees_constraint, is_fully_overlapping, \
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_every_shift_has_an_assigned_employee():
    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])
    test_employee2 = Employee("test2", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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
    shift_start_time_for_test = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])
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
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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


def test_verify_no_optimal_solution_when_there_are_more_shifts_then_max_working_shifts_for_one_employee():
    shift_start_time_for_test = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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
        employees.append(Employee(f"{_}", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[]))

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


def test_no_optimal_solution_when_the_closing_shift_and_the_next_shift_are_too_close_to_each_other():
    minimum_time_between_shifts = datetime.timedelta(hours=9)
    shift_duration = datetime.timedelta(hours=random.random())
    start_closing_shift_time = datetime.datetime(2023, 12, 12, 18, 0)

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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


def test_new_employees_can_work_parallel_shifts_with_senior_employees():
    main_shift_start_time = datetime.datetime(2023, 12, 12, 9, 0)
    shift_duration = datetime.timedelta(hours=4)

    """
    start shifts and end shifts

    |main shift|
    |support_shift1    |
    |support_shift2        |
                |support_shift3    |
    """

    main_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=main_shift_start_time + shift_duration)

    support_shift1_end_time = main_shift.end_time + shift_duration  # A double shift
    support_shift_1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=main_shift_start_time, end_time=support_shift1_end_time)

    support_shit2_end_time = support_shift_1.end_time + shift_duration  # A triple shift
    support_shift_2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=main_shift_start_time, end_time=support_shit2_end_time)

    support_shift3_start_time = main_shift.end_time
    support_shit3_end_time = support_shit2_end_time + shift_duration
    support_shift_3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=support_shift3_start_time, end_time=support_shit3_end_time)

    senior_employee = Employee("senior_employee", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])
    new_employee1 = Employee("new_employee1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id=uuid4(), preferences=[])
    new_employee2 = Employee("new_employee2", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id=uuid4(), preferences=[])

    shifts = [main_shift, support_shift_1, support_shift_2, support_shift_3]
    employees = [senior_employee, new_employee1, new_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    add_prevent_new_employees_from_working_parallel_shifts_together(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status == cp_model.OPTIMAL)

    senior_employee_working_main_shift_key = ShiftCombinationsKey(senior_employee.employee_id, main_shift.shift_id)
    senior_employee_working_support_shift3_key = ShiftCombinationsKey(senior_employee.employee_id, support_shift_3.shift_id)
    senior_employee_working_support_shift1_key = ShiftCombinationsKey(senior_employee.employee_id, support_shift_1.shift_id)
    senior_employee_working_support_shift2_key = ShiftCombinationsKey(senior_employee.employee_id, support_shift_2.shift_id)

    assert solver.Value(all_shifts[senior_employee_working_main_shift_key]) == True
    assert solver.Value(all_shifts[senior_employee_working_support_shift3_key]) == True
    assert solver.Value(all_shifts[senior_employee_working_support_shift1_key]) == False
    assert solver.Value(all_shifts[senior_employee_working_support_shift2_key]) == False


def test_new_employees_cannot_work_parallel_shift_without_at_least_one_employee_that_is_not_new():
    main_shift_start_time = datetime.datetime(2023, 12, 12, 9, 0)
    shift_duration = datetime.timedelta(hours=4)

    """
    start shifts and end shifts

    |main shift|
    |support_shift1    |
    """

    main_shift = Shift("main_shift", shift_type=ShiftTypesEnum.EVENING, start_time=main_shift_start_time, end_time=main_shift_start_time + shift_duration)

    support_shift1_end_time = main_shift.end_time + shift_duration  # A double shift
    support_shift_1 = Shift("support_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=main_shift_start_time, end_time=support_shift1_end_time)

    new_employee1 = Employee("new_emp1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id="new_emp1", preferences=[])
    new_employee2 = Employee("new_emp2", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id="new_emp2", preferences=[])
    senior_employee = Employee("sen_emp", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, employee_id="sen_emp", preferences=[])

    shifts = [main_shift, support_shift_1]
    employees = [new_employee1, new_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    new_employees_in_each_shifts, non_new_employees_in_each_shifts,non_new_emps_working_in_all_shift_permutations,any_perm_for_each_shift = add_prevent_new_employees_from_working_parallel_shifts_together(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    vars = list(new_employees_in_each_shifts.values()) + list(non_new_employees_in_each_shifts.values()) + list(non_new_emps_working_in_all_shift_permutations.values()) + list(all_shifts.values()) + list(any_perm_for_each_shift.values())
    solution_printer = VarArraySolutionPrinter(vars)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)
    assert (status != cp_model.OPTIMAL)


def test_employees_can_work_non_overlapping_shifts():
    """
    |shift1     | |shift2       |
    """
    test_shift_start_time = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=test_shift_start_time, end_time=test_shift_start_time + shift_duration)
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift.end_time + shift_duration, end_time=test_shift.end_time + (shift_duration * 2))

    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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
    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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
    test_employee = Employee("test", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid4(), preferences=[])

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


def test_senior_employee_and_new_employee_in_parallel_shifts():
    shift_time_duration = datetime.timedelta(hours=4)
    main_shift_start_time = datetime.datetime(2023, 12, 12, 12, 0) # 12:00:00 16:00:00
    main_shift_end_time = main_shift_start_time + shift_time_duration
    support_shift1_start_time = main_shift_start_time - datetime.timedelta(hours=2)
    support_shift1_end_time = support_shift1_start_time + shift_time_duration
    support_shift2_start_time = support_shift1_end_time
    support_shift2_end_time = support_shift2_start_time+ shift_time_duration

    """
    start shifts and end shifts
                12:00:00-16:00:00
                 |main shift|
    10:00:00-14:00:00  14:00:00-18:00:00
    |support_shift1    |support_shift2        |
    """

    main_shift = Shift("main_shift", shift_type=ShiftTypesEnum.EVENING, start_time=main_shift_start_time, end_time=main_shift_end_time)

    support_shift_1 = Shift("shift1", shift_type=ShiftTypesEnum.CLOSING, start_time=support_shift1_start_time, end_time=support_shift1_end_time)

    support_shift_2 = Shift("shift2", shift_type=ShiftTypesEnum.CLOSING, start_time=support_shift2_start_time, end_time=support_shift2_end_time)

    senior_employee = Employee("senior_employee", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, "senior_employee", preferences=[])

    new_employee1 = Employee("new_employee1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, "new_employee1", preferences=[])

    shifts = [support_shift_1, support_shift_2, main_shift]
    employees = [new_employee1, senior_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_new_employees_from_working_parallel_shifts_together(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)

    new_employees_in_each_shifts, non_new_employees_in_each_shifts, non_new_emps_working_in_all_shift_permutations, any_perm_for_each_shift = add_prevent_new_employees_from_working_parallel_shifts_together(
        shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    vars = list(new_employees_in_each_shifts.values()) + list(non_new_employees_in_each_shifts.values()) + list(
        non_new_emps_working_in_all_shift_permutations.values()) + list(all_shifts.values()) + list(
        any_perm_for_each_shift.values())
    solution_printer = VarArraySolutionPrinter(vars)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)

    """
    # For visually testing the solver, to see if the assignments are as expected.
    solutions = solution_printer.get_solutions()
    print("-----solutions-----")
    for solution in solutions.optimal_solutions:
        for key, val in solution.items():
            print(f"{key} = {val}")
        print("")
    """

    assert (status == cp_model.OPTIMAL)

    new_employee_working_main_shift = all_shifts[ShiftCombinationsKey(new_employee1.employee_id, main_shift.shift_id)]
    assert solver.Value(new_employee_working_main_shift) == True

    senior_employee_working_support_shift1 = all_shifts[ShiftCombinationsKey(senior_employee.employee_id, support_shift_1.shift_id)]
    assert solver.Value(senior_employee_working_support_shift1) == True

    senior_employee_working_support_shift2 = all_shifts[ShiftCombinationsKey(senior_employee.employee_id, support_shift_2.shift_id)]
    assert solver.Value(senior_employee_working_support_shift2) == True


def test_shifts_are_parallel_to_each_other():
    main_shift_start_time = datetime.datetime(2023, 12, 12, 9)

    main_shift = Shift("main_shitf", shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=main_shift_start_time + datetime.timedelta(hours=4))
    support_shift1 = Shift("support_shift1", shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=main_shift_start_time + datetime.timedelta(hours=2))
    support_shift2 = Shift("support_shift2", shift_type=ShiftTypesEnum.MORNING, start_time=support_shift1.end_time, end_time=main_shift.end_time)
    support_shift3 = Shift("support_shift3", shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=support_shift1.end_time)

    assert(False == is_fully_overlapping(main_shift, [support_shift2]))
    assert(False == is_fully_overlapping(main_shift, [support_shift1]))
    assert(False == is_fully_overlapping(main_shift,[support_shift3]))
    assert(True == is_fully_overlapping(main_shift, [support_shift1, support_shift2]))
    assert(True == is_fully_overlapping(main_shift, [support_shift3, support_shift2]))
    assert(False == is_fully_overlapping(main_shift, [support_shift3, support_shift1]))
    assert(True == is_fully_overlapping(main_shift, [support_shift1, support_shift3, support_shift2]))


def test_solver_assignments_for_variables_in_the_model_are_as_expected():
    main_shift_start_time = datetime.datetime(2023, 12, 12, 9, 0)
    shift_duration = datetime.timedelta(hours=4)

    """
    start shifts and end shifts

    |main shift|
    |support_shift1    |
    """

    main_shift = Shift("main_shift", shift_type=ShiftTypesEnum.EVENING, start_time=main_shift_start_time, end_time=main_shift_start_time + shift_duration)

    support_shift1_end_time = main_shift.end_time + shift_duration  # A double shift

    support_shift_1 = Shift("support_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=main_shift_start_time, end_time=support_shift1_end_time)

    new_employee1 = Employee("new_emp1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id="new_emp1", preferences=[])
    senior_employee = Employee("sen_emp", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, employee_id="sen_emp", preferences=[])

    shifts = [main_shift, support_shift_1]
    employees = [senior_employee, new_employee1]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    new_employees_in_each_shifts, non_new_employees_in_each_shifts, non_new_emps_working_in_all_shift_permutations, any_perm_for_each_shift = add_prevent_new_employees_from_working_parallel_shifts_together(
        shifts, employees, model, all_shifts)

    vars = list(new_employees_in_each_shifts.values()) + list(non_new_employees_in_each_shifts.values()) + list(
        non_new_emps_working_in_all_shift_permutations.values()) + list(all_shifts.values()) + list(
        any_perm_for_each_shift.values())

    solver = cp_model.CpSolver()

    solution_printer = VarArraySolutionPrinter(vars)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)

    solutions = solution_printer.get_solutions()
    assert (status == cp_model.OPTIMAL)
    for solution in solutions.optimal_solutions:
        key_new_emps_in_main_shift = "new_emps_main_shift"
        key_new_emps_in_support_shift = "new_emps_support_shift"
        key_non_new_emps_in_support_shift = "non_new_emps_support_shift"
        key_non_new_emps_in_main_shift = "non_new_emps_main_shift"
        key_fully_non_new_emps_in_support_shift = "fully_non_new_emps_perm_support_shift"

        assert(solution[key_new_emps_in_main_shift] == True)
        assert(solution[key_non_new_emps_in_support_shift] == True)
        assert(solution[key_new_emps_in_support_shift] == False)
        assert(solution[key_non_new_emps_in_main_shift] == False)
        assert(solution[key_fully_non_new_emps_in_support_shift] == True)


def test_overlapping_shifts_where_shift_starts_in_the_same_time():
    """
    [ A ]
    [ B   ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a.end_time + shift_duration)

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)

    pass


def test_overlapping_shifts_where_shift_ends_in_the_same_time():
    """
      [ A ]
    [ B   ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time - shift_duration, end_time=shift_a.end_time)

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shift_starts_before_other_shift_and_ends_before_other_shift_ends():
    """
    [ A ]
      [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time + (shift_duration / 2), end_time=shift_a.end_time + (shift_duration / 2))

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shift_starts_after_other_shift_starts_and_ends_after_other_shift_ends():
    """
      [ A ]
    [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time - (shift_duration / 2), end_time=shift_a.end_time - (shift_duration / 2))

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_other_shift_starts_when_shift_ends():
    """
    [ A ]
        [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a.end_time, end_time=shift_a.end_time + shift_duration)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shift_starts_when_other_shift_ends():
    """
        [ A ]
    [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a.start_time - shift_duration, end_time=shift_a.start_time)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shifts_dont_overlap_at_all():
    """
    [ A ]
           [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a.end_time + shift_duration, end_time=shift_a.end_time + shift_duration + shift_duration)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)
