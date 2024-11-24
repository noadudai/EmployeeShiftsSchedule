import datetime
from uuid import uuid4

from ortools.sat.python import cp_model
from .schedule_solution_collector import ScheduleSolutionCollector

from constraints_file import generate_shift_employee_combinations, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_prevent_new_employees_from_working_parallel_shifts_together, add_exactly_one_employee_per_shift_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


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

    senior_employee = Employee("senior_employee", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)
    new_employee1 = Employee("new_employee1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)
    new_employee2 = Employee("new_employee2", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id=uuid4(), position=EmployeePositionEnum.part_timer)

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

    new_employee1 = Employee("new_emp1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id="new_emp1", position=EmployeePositionEnum.part_timer)
    new_employee2 = Employee("new_emp2", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id="new_emp2", position=EmployeePositionEnum.part_timer)

    shifts = [main_shift, support_shift_1]
    employees = [new_employee1, new_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    new_employees_in_each_shifts, non_new_employees_in_each_shifts,non_new_emps_working_in_all_shift_permutations,any_perm_for_each_shift = add_prevent_new_employees_from_working_parallel_shifts_together(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    vars = list(new_employees_in_each_shifts.values()) + list(non_new_employees_in_each_shifts.values()) + list(non_new_emps_working_in_all_shift_permutations.values()) + list(all_shifts.values()) + list(any_perm_for_each_shift.values())
    solution_printer = ScheduleSolutionCollector(vars)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)
    assert (status != cp_model.OPTIMAL)


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

    senior_employee = Employee("senior_employee", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, "senior_employee", position=EmployeePositionEnum.part_timer)

    new_employee1 = Employee("new_employee1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, "new_employee1", position=EmployeePositionEnum.part_timer)

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
    solution_printer = ScheduleSolutionCollector(vars)
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

    new_employee1 = Employee("new_emp1", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, employee_id="new_emp1", position=EmployeePositionEnum.part_timer)
    senior_employee = Employee("sen_emp", EmployeePriorityEnum.LOW, EmployeeStatusEnum.senior_employee, employee_id="sen_emp", position=EmployeePositionEnum.part_timer)

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

    solution_printer = ScheduleSolutionCollector(vars)
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
