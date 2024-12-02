import datetime
import random
import uuid

from ortools.sat.python import cp_model

from models.employees.employee_preferences.days_preference import DaysRangePreference, DaysPreference
from models.employees.employee_preferences.shift_preferences_by_id import ShiftPreferencesById
from .schedule_solution_collector import ScheduleSolutionCollector

from constraints_file import generate_shift_employee_combinations, \
    add_aspire_to_maximize_all_employees_preferences_constraint, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_preferences.preferences import Preferences
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_an_employee_is_not_working_in_a_day_he_can_not_work():
    shift_duration = datetime.timedelta(minutes=random.random())
    shift_emp_with_day_off_cannot_work = Shift(shift_id="shift_emp_with_day_off_cannot_work", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + shift_duration)

    today = datetime.datetime.today().date()
    emp_preferences = Preferences(days_cannot_work=DaysPreference([DaysRangePreference(datetime.datetime(today.year, today.month, today.day, 0), datetime.datetime(today.year, today.month, today.day, 23, 59))]))
    # emp_preferences = Preferences(days_cannot_work=DaysPreference([datetime.date.today()]))

    emp_with_day_off = Employee(name="emp_with_day_off", employee_id="emp_with_day_off", preferences=emp_preferences)
    test_employee = Employee(name="test_employee", employee_id="test_employee")

    employees = [emp_with_day_off, test_employee]
    shifts = [shift_emp_with_day_off_cannot_work]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(test_employee.employee_id, shift_emp_with_day_off_cannot_work.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_day_off.employee_id, shift_emp_with_day_off_cannot_work.shift_id)]) == False)


def test_an_employee_is_not_working_in_a_day_he_prefers_not_to_work():
    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))
    shift2 = Shift(shift_id="shift2", shift_type=ShiftTypesEnum.MORNING, start_time=shift1.end_time, end_time=shift1.end_time + datetime.timedelta(minutes=30))

    today = datetime.datetime.today().date()
    emp_with_a_day_off_request_preferences = Preferences(days_prefer_not_to_work=DaysPreference([DaysRangePreference(datetime.datetime(today.year, today.month, today.day, 0), datetime.datetime(today.year, today.month, today.day, 23, 59))]))

    emp_with_a_day_off_request = Employee(name="emp_with_a_day_off_request", employee_id="emp_with_a_day_off_request", preferences=emp_with_a_day_off_request_preferences)
    emp_with_no_preferences = Employee(name="emp_with_no_preferences", employee_id="emp_with_no_preferences")

    employees = [emp_with_a_day_off_request, emp_with_no_preferences]
    shifts = [shift1, shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()

    all_assignments = [all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for employee in employees for shift in shifts]

    solution_collection = ScheduleSolutionCollector(emp_shift_assignments=all_assignments)
    status = solver.Solve(model, solution_collection)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift2.shift_id)]) == True)


def test_a_high_priority_employee_gets_the_shift_instead_of_a_less_priority_employee():
    overlapping_shifts_start_time = datetime.datetime.now()
    overlapping_shifts_end_time = datetime.datetime.now() + datetime.timedelta(minutes=30)

    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=overlapping_shifts_start_time, end_time=overlapping_shifts_end_time)
    shift2 = Shift(shift_id="shift2", shift_type=ShiftTypesEnum.MORNING, start_time=overlapping_shifts_start_time, end_time=overlapping_shifts_end_time)

    emps_wants_shift1_preferences = Preferences(shifts_prefer_by_id=ShiftPreferencesById([shift1.shift_id]))
    medium_priority_employee = Employee(name="emp", employee_id="medium_priority_employee", priority=EmployeePriorityEnum.MEDIUM, preferences=emps_wants_shift1_preferences)
    highest_priority_employee = Employee(name="highest_priority_employee", employee_id="highest_priority_employee", preferences=emps_wants_shift1_preferences, priority=EmployeePriorityEnum.HIGHEST)

    employees = [highest_priority_employee, medium_priority_employee]
    shifts = [shift1, shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()

    all_assignments = [all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for employee in employees for shift in shifts]

    solution_collection = ScheduleSolutionCollector(emp_shift_assignments=all_assignments)
    status = solver.Solve(model, solution_collection)

    assert (status == cp_model.OPTIMAL)

    assert (solver.Value(all_shifts[ShiftCombinationsKey(highest_priority_employee.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(highest_priority_employee.employee_id, shift2.shift_id)]) == False)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(medium_priority_employee.employee_id, shift2.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(medium_priority_employee.employee_id, shift1.shift_id)]) == False)


def test_an_emp_who_prefers_not_to_work_is_working_so_a_different_emp_with_a_day_off_will_not_work():
    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    today = datetime.datetime.today().date()
    same_days_range = DaysPreference([DaysRangePreference(datetime.datetime(today.year, today.month, today.day, 0), datetime.datetime(today.year, today.month, today.day, 23, 59))])

    emp_with_day_off_preferences = Preferences(days_cannot_work=same_days_range)
    emp_wants_day_off_preferences = Preferences(days_prefer_not_to_work=same_days_range)

    emp_with_day_off = Employee(name="emp_with_day_off", employee_id="emp_with_day_off", position=EmployeePositionEnum.full_timer, preferences=emp_with_day_off_preferences)
    emp_wants_day_off = Employee(name="emp_wants_day_off", employee_id="test_employee", position=EmployeePositionEnum.full_timer, preferences=emp_wants_day_off_preferences)

    employees = [emp_with_day_off, emp_wants_day_off]
    shifts = [shift1]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_wants_day_off.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_day_off.employee_id, shift1.shift_id)]) == False)


def test_an_emp_who_does_not_have_preferences_is_working_so_other_employees_can_have_a_day_off():
    shift1 = Shift(shift_id="shift1", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))
    shift2 = Shift(shift_id="shift2", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    today = datetime.datetime.today().date()
    same_days_range = DaysPreference([DaysRangePreference(datetime.datetime(today.year, today.month, today.day, 0), datetime.datetime(today.year, today.month, today.day, 23, 59))])

    emp_with_day_off_preferences = Preferences(days_cannot_work=same_days_range)
    emp_wants_day_off_preferences = Preferences(days_prefer_not_to_work=same_days_range)

    emp_with_day_off = Employee(name="emp_with_day_off", employee_id="emp_with_day_off", preferences=emp_with_day_off_preferences)
    emp_wants_day_off = Employee(name="emp_wants_day_off", employee_id="emp_wants_day_off", preferences=emp_wants_day_off_preferences)
    emp_with_no_preferences = Employee(name="emp_with_no_preferences", employee_id="emp_with_no_preferences")

    employees = [emp_with_day_off, emp_wants_day_off, emp_with_no_preferences]
    shifts = [shift1, shift2]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift1.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp_with_no_preferences.employee_id, shift2.shift_id)]) == True)


def test_no_schedule_when_there_is_only_one_shift_and_the_employee_cannot_work_it():
    morning_shift = Shift(shift_id=uuid.uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=random.random()))

    emp_preferences = Preferences(shifts_cannot_work=ShiftPreferencesById([morning_shift.shift_id]))

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

    emp_preferences = Preferences(shifts_cannot_work=ShiftPreferencesById([morning_shift.shift_id]))

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
