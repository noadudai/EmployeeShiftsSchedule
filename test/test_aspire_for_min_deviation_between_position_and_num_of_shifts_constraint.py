import datetime
import random

from ortools.sat.python import cp_model
from .schedule_solution_collector import ScheduleSolutionCollector

from constraints_file import generate_shift_employee_combinations, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_exactly_one_employee_per_shift_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum
from test.test_helper_functions import get_employees_shifts_assignments


def test_full_timer_and_part_timer_gets_their_positions_amount_of_shifts():
    test_shift1_start_time = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_shift1 = Shift("test_shift1", shift_type=ShiftTypesEnum.MORNING, start_time=test_shift1_start_time, end_time=test_shift1_start_time + shift_duration)
    test_shift2 = Shift("test_shift2", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift1.end_time, end_time=test_shift1.end_time + shift_duration)
    test_shift3 = Shift("test_shift3", shift_type=ShiftTypesEnum.MORNING, start_time=test_shift2.end_time,  end_time=test_shift2.end_time + shift_duration)
    test_shift4 = Shift("test_shift4", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift3.end_time, end_time=test_shift3.end_time + shift_duration)

    full_timer_employee = Employee("full_timer_employee", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="full_timer_employee", position=EmployeePositionEnum.full_timer)
    part_timer_employee = Employee("part_timer_employee", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="part_timer_employee", position=EmployeePositionEnum.part_timer)

    employees = [full_timer_employee, part_timer_employee]
    shifts = [test_shift1, test_shift2, test_shift3, test_shift4]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    emp_shift_assignments = get_employees_shifts_assignments(all_shifts, employees, shifts, solver)

    assert len(emp_shift_assignments["full_timer_employee"]) == full_timer_employee.position.value
    assert len(emp_shift_assignments["part_timer_employee"]) == part_timer_employee.position.value


def test_the_2_extra_shifts_aside_from_the_positions_shifts_amount_are_divided_evenly_between_the_employees():
    test_shift1_start_time = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_shift1 = Shift("test_shift1", shift_type=ShiftTypesEnum.MORNING, start_time=test_shift1_start_time, end_time=test_shift1_start_time + shift_duration)
    test_shift2 = Shift("test_shift2", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift1.end_time, end_time=test_shift1.end_time + shift_duration)
    test_shift3 = Shift("test_shift3", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift2.end_time,  end_time=test_shift2.end_time + shift_duration)
    test_shift4 = Shift("test_shift4", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift3.end_time, end_time=test_shift3.end_time + shift_duration)
    test_shift5 = Shift("test_shift5", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift4.end_time, end_time=test_shift4.end_time + shift_duration)
    test_shift6 = Shift("test_shift6", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift5.end_time, end_time=test_shift5.end_time + shift_duration)

    full_timer_employee = Employee("full_timer_employee", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="full_timer_employee", position=EmployeePositionEnum.full_timer)
    part_timer_employee = Employee("part_timer_employee", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="part_timer_employee", position=EmployeePositionEnum.part_timer)

    employees = [full_timer_employee, part_timer_employee]
    shifts = [test_shift1, test_shift2, test_shift3, test_shift4, test_shift5, test_shift6]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    vars = add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    solution_printer = ScheduleSolutionCollector(vars)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)

    assert (status == cp_model.OPTIMAL)

    emp_shift_assignments = get_employees_shifts_assignments(all_shifts, employees, shifts, solver)

    assert len(emp_shift_assignments["full_timer_employee"]) == full_timer_employee.position.value + 1
    assert len(emp_shift_assignments["part_timer_employee"]) == part_timer_employee.position.value + 1


def test_the_shifts_are_divided_between_the_employees_and_no_employee_works_more_than_one_shift_than_the_other():
    test_shift1_start_time = datetime.datetime(2023, 12, 11, 9, 30)
    shift_duration = datetime.timedelta(hours=random.random())
    test_shift1 = Shift("test_shift1", shift_type=ShiftTypesEnum.MORNING, start_time=test_shift1_start_time, end_time=test_shift1_start_time + shift_duration)
    test_shift2 = Shift("test_shift2", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift1.end_time, end_time=test_shift1.end_time + shift_duration)
    test_shift3 = Shift("test_shift3", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift2.end_time,  end_time=test_shift2.end_time + shift_duration)
    test_shift4 = Shift("test_shift4", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift3.end_time, end_time=test_shift3.end_time + shift_duration)
    test_shift5 = Shift("test_shift5", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift4.end_time, end_time=test_shift4.end_time + shift_duration)
    test_shift6 = Shift("test_shift6", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift5.end_time, end_time=test_shift5.end_time + shift_duration)
    test_shift7 = Shift("test_shift7", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=test_shift5.end_time, end_time=test_shift5.end_time + shift_duration)

    full_timer_employee = Employee("full_timer_employee", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="full_timer_employee", position=EmployeePositionEnum.full_timer)
    part_timer_employee = Employee("part_timer_employee", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="part_timer_employee", position=EmployeePositionEnum.part_timer)

    employees = [full_timer_employee, part_timer_employee]
    shifts = [test_shift1, test_shift2, test_shift3, test_shift4, test_shift5, test_shift6, test_shift7]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    vars = add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    solution_printer = ScheduleSolutionCollector(vars)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)

    assert (status == cp_model.OPTIMAL)

    emp_shift_assignments = get_employees_shifts_assignments(all_shifts, employees, shifts, solver)

    full_timer_shifts_deviation = len(emp_shift_assignments["full_timer_employee"]) - full_timer_employee.position.value
    part_timer_deviation = len(emp_shift_assignments["part_timer_employee"]) - part_timer_employee.position.value

    full_timer_deviation_with_2_more_shifts = full_timer_shifts_deviation + 2
    part_timer_have_one_more_shift_deviation_then_the_full_timer = full_timer_deviation_with_2_more_shifts > part_timer_deviation > full_timer_shifts_deviation

    assert part_timer_have_one_more_shift_deviation_then_the_full_timer
