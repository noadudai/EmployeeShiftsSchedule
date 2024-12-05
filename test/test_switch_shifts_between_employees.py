import datetime
import random

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint, \
    add_an_employees_switch_shifts_after_schedule_created_constraint
from models.employees.employee import Employee
from models.employees.employee_preferences.employees_shifts_preferences import EmployeesShiftsPreferences
from models.employees.employee_preferences.emps_shifts_switch_request import EmployeesShiftSwitchRequest
from models.employees.employee_preferences.shifts_preference_by_id import ShiftIdPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_2_employees_can_switch_shifts():
    employee1 = Employee(name="employee1", employee_id="employee1")
    employee2 = Employee(name="employee2", employee_id="employee2")

    employees = [employee1, employee2]

    shifts_start_time = datetime.datetime.now()
    shifts_end_time = datetime.datetime.now() + datetime.timedelta(minutes=random.random())

    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=shifts_start_time, end_time=shifts_end_time)
    shift2 = Shift(shift_id="shift2", shift_type=ShiftTypesEnum.MORNING, start_time=shifts_start_time, end_time=shifts_end_time)

    shifts = [shift1, shift2]
    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    assert (status == cp_model.OPTIMAL)

    if solver.Value(all_shifts[ShiftCombinationsKey(employee1.employee_id, shift1.shift_id)]) == 1:
        emps_who_wants_to_switch = EmployeesShiftSwitchRequest(emp_1_id=employee1.employee_id, emp_1_has_shift=shift1.shift_id, emp_2_id=employee2.employee_id, emp_2_has_shift=shift2.shift_id)

        result = add_an_employees_switch_shifts_after_schedule_created_constraint(emps_who_wants_to_switch, constraint_model, all_shifts, solver, employees, shifts)

        assert (result != False)
        assert (result.schedule[shift1.shift_id] != employee1.employee_id)
        assert (result.schedule[shift1.shift_id] == employee2.employee_id)
        assert (result.schedule[shift2.shift_id] == employee1.employee_id)
        assert (result.schedule[shift2.shift_id] != employee2.employee_id)
    else:
        emps_who_wants_to_switch = EmployeesShiftSwitchRequest(emp_1_id=employee1.employee_id, emp_1_has_shift=shift2.shift_id, emp_2_id=employee2.employee_id, emp_2_has_shift=shift1.shift_id)

        result = add_an_employees_switch_shifts_after_schedule_created_constraint(emps_who_wants_to_switch, constraint_model, all_shifts, solver, employees, shifts)

        assert (result != False)
        assert (result.schedule[shift1.shift_id] == employee1.employee_id)
        assert (result.schedule[shift1.shift_id] != employee2.employee_id)
        assert (result.schedule[shift2.shift_id] != employee1.employee_id)
        assert (result.schedule[shift2.shift_id] == employee2.employee_id)


def test_2_employees_cannot_switch_shifts_because_one_of_the_employees_is_not_trained_to_do_the_switched_shift():
    emp_can_work_all_shifts = Employee(name="emp_can_work_all_shifts", priority=EmployeePriorityEnum.HIGHEST, employee_id="emp_can_work_all_shifts", shift_types_trained_to_do=[ShiftTypesEnum.MORNING, ShiftTypesEnum.CLOSING])
    emp_can_work_only_morning_shift = Employee(name="emp_can_work_only_morning_shift", employee_id="emp_can_work_only_morning_shift", shift_types_trained_to_do=[ShiftTypesEnum.MORNING])

    employees = [emp_can_work_all_shifts, emp_can_work_only_morning_shift]

    shifts_start_time = datetime.datetime.now()
    shifts_end_time = datetime.datetime.now() + datetime.timedelta(minutes=random.random())

    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=shifts_start_time, end_time=shifts_end_time)
    closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=shifts_start_time, end_time=shifts_end_time)

    shifts = [morning_shift, closing_shift]
    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_can_work_only_morning_shift.employee_id, morning_shift.shift_id)]))

    emps_who_wants_to_switch = EmployeesShiftSwitchRequest(emp_1_id=emp_can_work_only_morning_shift.employee_id, emp_1_has_shift=morning_shift.shift_id, emp_2_id=emp_can_work_all_shifts.employee_id, emp_2_has_shift=closing_shift.shift_id)

    result = add_an_employees_switch_shifts_after_schedule_created_constraint(emps_who_wants_to_switch, constraint_model, all_shifts, solver, employees, shifts)

    assert (result == False)


def test_2_employees_switch_shifts_even_when_its_a_shift_the_employee_wanted():
    shifts_start_time = datetime.datetime.now()
    shifts_end_time = datetime.datetime.now() + datetime.timedelta(minutes=random.random())

    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=shifts_start_time, end_time=shifts_end_time)
    closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=shifts_start_time, end_time=shifts_end_time)

    employee2s_preferences = EmployeesShiftsPreferences(shifts_wants_to_work=ShiftIdPreference([morning_shift.shift_id]))

    employee1 = Employee(name="employee1", employee_id="employee1")
    employee_wants_morning_shift = Employee(name="employee_wants_morning_shift", priority=EmployeePriorityEnum.HIGH, employee_id="employee_wants_morning_shift", shifts_preferences=employee2s_preferences)

    employees = [employee1, employee_wants_morning_shift]

    shifts = [morning_shift, closing_shift]
    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(employee_wants_morning_shift.employee_id, morning_shift.shift_id)]) == 1)

    emps_who_wants_to_switch = EmployeesShiftSwitchRequest(emp_1_id=employee_wants_morning_shift.employee_id, emp_1_has_shift=morning_shift.shift_id, emp_2_id=employee1.employee_id, emp_2_has_shift=closing_shift.shift_id)

    result = add_an_employees_switch_shifts_after_schedule_created_constraint(emps_who_wants_to_switch, constraint_model, all_shifts, solver, employees, shifts)

    assert (result != False)
    assert (result.schedule[morning_shift.shift_id] == employee1.employee_id)
    assert (result.schedule[morning_shift.shift_id] != employee_wants_morning_shift.employee_id)
    assert (result.schedule[closing_shift.shift_id] == employee_wants_morning_shift.employee_id)
    assert (result.schedule[closing_shift.shift_id] != employee1.employee_id)
