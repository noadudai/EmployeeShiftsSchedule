import datetime
import random
import uuid

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, \
    add_aspire_to_maximize_all_employees_preferences_constraint, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint
from models.employees.employee import Employee
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_highest_priority_emp_gets_the_shift_he_wants_and_not_the_mid_priority_emp():
    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))
    closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))

    highest_priority_emp_preferences = Preferences(shifts_has_to_work_in_days=[ShiftsPreference(datetime.datetime.today().date(), [ShiftTypesEnum.MORNING, ShiftTypesEnum.CLOSING])])
    highest_priority_emp = Employee(name="highest_priority_emp", priority=EmployeePriorityEnum.HIGHEST, employee_id="highest_priority_emp", preferences=highest_priority_emp_preferences)
    emp_preferences = Preferences(shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.datetime.today().date(), [ShiftTypesEnum.MORNING])])
    emp = Employee(name="emp", employee_id="test_employee", preferences= emp_preferences)

    employees = [highest_priority_emp, emp]
    shifts = [morning_shift, closing_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(highest_priority_emp.employee_id, morning_shift.shift_id)]) == True)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(emp.employee_id, closing_shift.shift_id)]) == False)
    assert (solver.Value(all_shifts[ShiftCombinationsKey(highest_priority_emp.employee_id, closing_shift.shift_id)]) == True)


# The highest priority employee wants 2 parallel shifts, something he knows he cant have.
def test_no_schedule_because_a_higher_emp_wants_parallel_shifts():
    morning_shift = Shift(shift_id="morning_shift", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))
    closing_shift = Shift(shift_id="closing_shift", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime.now(), end_time=datetime.datetime.now() + datetime.timedelta(minutes=30))

    emp_preferences = Preferences(shifts_has_to_work_in_days=[ShiftsPreference(datetime.datetime.today().date(), [ShiftTypesEnum.MORNING, ShiftTypesEnum.CLOSING])])
    highest_priority_emp = Employee(name="highest_priority_emp", priority=EmployeePriorityEnum.HIGHEST, employee_id="highest_priority_emp", preferences=emp_preferences)
    emp = Employee(name="emp", employee_id="test_employee")

    employees = [highest_priority_emp, emp]
    shifts = [morning_shift, closing_shift]
    model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)
