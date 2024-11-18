import datetime
import random
import uuid

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, \
    add_aspire_to_maximize_all_employees_preferences_constraint, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_preferences.day_preference import DayOffPreference
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_an_employee_is_not_working_in_a_day_he_can_not_work():
    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))
    emp_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date.today())])
    emp_with_day_off = Employee(name="emp_with_day_off", employee_id="emp_with_day_off", preferences=emp_preferences)
    emp = Employee(name="emp", employee_id="test_employee")

    employees = [emp_with_day_off, emp]
    shifts = [shift1]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_day_off.employee_id, shift1.shift_id)]) == False)


def test_an_employee_is_not_working_in_a_day_he_prefers_not_to_work():
    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))
    shift2 = Shift(shift_id="shift2", shift_type=ShiftTypesEnum.MORNING, start_time=shift1.end_time, end_time=shift1.end_time + datetime.timedelta(minutes=30))
    emp_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date.today())])
    emp_with_a_day_off_request = Employee(name="emp_with_a_day_off_request", employee_id="emp_with_a_day_off_request", preferences=emp_preferences)
    emp_with_no_preferences = Employee(name="emp_with_no_preferences", employee_id="test_employee")

    employees = [emp_with_a_day_off_request, emp_with_no_preferences]
    shifts = [shift1, shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    model.AddHint(all_shifts[ShiftCombinationsKey(emp_with_a_day_off_request.employee_id, shift1.shift_id)], 0)
    model.AddHint(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift1.shift_id)], 1)
    model.AddHint(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift2.shift_id)], 1)

    solver = cp_model.CpSolver()
    solver.parameters.fix_variables_to_their_hinted_value = True
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift2.shift_id)]) == True)


def test_an_employee_gets_his_preferred_shifts():
    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))
    closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))

    emp_preferences = Preferences(shifts_prefer_to_work_in_days=ShiftsPreference(["morning_shift"]))
    emp = Employee(name="emp", employee_id="test_employee", priority=EmployeePriorityEnum.MEDIUM)
    emp_wants_shift1 = Employee(name="emp_wants_shift1", employee_id="emp_wants_shift1", preferences=emp_preferences, priority=EmployeePriorityEnum.HIGHEST)

    employees = [emp_wants_shift1, emp]
    shifts = [morning_shift, closing_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    model.AddHint(all_shifts[ShiftCombinationsKey(emp.employee_id, closing_shift.shift_id)], 1)

    solver = cp_model.CpSolver()
    solver.parameters.fix_variables_to_their_hinted_value = True
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp.employee_id, closing_shift.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_wants_shift1.employee_id, morning_shift.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_wants_shift1.employee_id, closing_shift.shift_id)]) == False)


def test_an_emp_who_prefers_not_to_work_is_working_so_a_different_emp_with_a_day_off_will_not_work():
    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    emp_with_day_off_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.datetime.today().date())])
    emp_wants_day_off_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.datetime.today().date())])

    emp_with_day_off = Employee(name="emp_with_day_off", employee_id="emp_with_day_off", position=EmployeePositionEnum.full_timer, preferences=emp_with_day_off_preferences)
    emp_wants_day_off = Employee(name="emp_wants_day_off", employee_id="test_employee", position=EmployeePositionEnum.full_timer, preferences=emp_wants_day_off_preferences)

    employees = [emp_with_day_off, emp_wants_day_off]
    shifts = [morning_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_wants_day_off.employee_id, morning_shift.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_day_off.employee_id, morning_shift.shift_id)]) == False)


def test_an_emp_who_does_not_have_preferences_is_working_so_other_employees_can_have_a_day_off():
    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))
    shift2 = Shift(shift_id="shift2", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    emp_with_day_off_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.datetime.today().date())])
    emp_wants_day_off_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.datetime.today().date())])

    emp_with_day_off = Employee(name="emp_with_day_off", employee_id="emp_with_day_off", preferences=emp_with_day_off_preferences)
    emp_wants_day_off = Employee(name="emp_wants_day_off", employee_id="emp_wants_day_off", preferences=emp_wants_day_off_preferences)
    emp_with_no_preferences = Employee(name="emp_with_no_preferences", employee_id="emp_with_no_preferences")

    employees = [emp_with_day_off, emp_wants_day_off, emp_with_no_preferences]
    shifts = [shift1, shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    model.AddHint(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift1.shift_id)], 1)
    model.AddHint(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift2.shift_id)], 1)

    solver = cp_model.CpSolver()
    solver.parameters.fix_variables_to_their_hinted_value = True
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift2.shift_id)]) == True)


def test_no_schedule_when_there_is_only_one_shift_and_the_employee_cannot_work_it():
    morning_shift = Shift(shift_id=uuid.uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    emp_preferences = Preferences(shifts_cannot_work=ShiftsPreference([morning_shift.shift_id]))

    emp_who_cannot_work_morning_shift_today = Employee(name="emp_who_cannot_work_morning_shift_today", employee_id=uuid.uuid4(), preferences=emp_preferences)

    employees = [emp_who_cannot_work_morning_shift_today]
    shifts = [morning_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)


def test_an_employee_who_cannot_work_a_specific_shift_is_not_working_it():
    morning_shift = Shift(shift_id=uuid.uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))
    morning_backup_shift = Shift(shift_id=uuid.uuid4(), shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    emp_preferences = Preferences(shifts_cannot_work=ShiftsPreference([morning_shift.shift_id]))

    emp_who_cannot_work_morning_shift_today = Employee(name="emp_who_cannot_work_morning_shift_today", employee_id=uuid.uuid4(), preferences=emp_preferences)
    emp = Employee(name="emp", employee_id=uuid.uuid4())

    employees = [emp_who_cannot_work_morning_shift_today, emp]
    shifts = [morning_shift, morning_backup_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    emp_who_cannot_work_morning_shift_not_working_morning_key = ShiftCombinationsKey(emp_who_cannot_work_morning_shift_today.employee_id, morning_shift.shift_id)
    emp_who_cannot_work_morning_shift_is_working_morning_backup_key = ShiftCombinationsKey(emp_who_cannot_work_morning_shift_today.employee_id, morning_backup_shift.shift_id)
    emp_is_working_morning_shift_key = ShiftCombinationsKey(emp.employee_id, morning_shift.shift_id)
    assert (solver.Value(all_shifts[emp_who_cannot_work_morning_shift_not_working_morning_key]) == False)
    assert (solver.Value(all_shifts[emp_is_working_morning_shift_key]) == True)
    assert (solver.Value(all_shifts[emp_who_cannot_work_morning_shift_is_working_morning_backup_key]) == True)
