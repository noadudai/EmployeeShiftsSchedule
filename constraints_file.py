import datetime
import itertools

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from models.employees.employee import Employee
from models.shifts.frozen_shift_combinations_key import FrozenShiftCombinationsKey
from models.shifts.shift import Shift


# Returns a dictionary that contains all the combinations of shifts and employees as: FrozenShiftCombinationsKey
# as a key, and the value will be an IntVar using "constraint_model.NewBoolVar"
def generate_shift_employee_combinations(employees: list[Employee], shifts: list[Shift], constraint_model: cp_model.CpModel) -> \
dict[FrozenShiftCombinationsKey, IntVar]:
    shift_combinations = {}
    for employee in employees:
        employee_id = employee.employee_id

        for shift in shifts:
            key = FrozenShiftCombinationsKey(employee_id, shift.shift_id)

            shift_combinations[key] = constraint_model.NewBoolVar(f"employee_{employee_id}_shift_{shift.shift_id}")

    return shift_combinations


# A constraint that ensures that there will be exactly one employee in each shift per day.
def add_exactly_one_employee_per_shift_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[FrozenShiftCombinationsKey, IntVar]) -> None:
    for shift in shifts:
        all_employees_working_this_shift = []

        for employee in employees:
            key = FrozenShiftCombinationsKey(employee.employee_id, shift.shift_id)
            all_employees_working_this_shift.append(shift_combinations[key])

        constraint_model.AddExactlyOne(all_employees_working_this_shift)


# A constraint that ensures that each employee works at most one shift per day.
def add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[FrozenShiftCombinationsKey, IntVar]) -> None:
    # Creating a dictionary that will hold a date as a key and all the shifts that starts in that date as values.
    date_shifts_dict: dict[datetime.date, list[Shift]] = {}
    shift_grouping_func = lambda shift: shift.start_time.date()
    shifts.sort(key=shift_grouping_func)

    for date, shifts__that_start_in_date in itertools.groupby(shifts, shift_grouping_func):
        date_shifts_dict[date] = list(shifts__that_start_in_date)

    for shifts_in_day in date_shifts_dict.values():
        for employee in employees:
            works_shifts_on_day: list[IntVar] = []
            for shift in shifts_in_day:
                key = FrozenShiftCombinationsKey(employee.employee_id, shift.shift_id)
                works_shifts_on_day.append(shift_combinations[key])

            constraint_model.AddAtMostOne(works_shifts_on_day)
