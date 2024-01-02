import datetime
import itertools
import more_itertools

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from models.employees.employee import Employee
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


# Returns a dictionary that contains all the combinations of shifts and employees as: FrozenShiftCombinationsKey
# as a key, and the value will be an IntVar using "constraint_model.NewBoolVar"
def generate_shift_employee_combinations(employees: list[Employee], shifts: list[Shift], constraint_model: cp_model.CpModel) -> \
dict[ShiftCombinationsKey, IntVar]:
    shift_combinations = {}
    for employee in employees:
        employee_id = employee.employee_id

        for shift in shifts:
            key = ShiftCombinationsKey(employee_id, shift.shift_id)

            shift_combinations[key] = constraint_model.NewBoolVar(f"employee_{employee_id}_shift_{shift.shift_id}")

    return shift_combinations


def add_exactly_one_employee_per_shift_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar]) -> None:
    for shift in shifts:
        all_employees_working_this_shift = []

        for employee in employees:
            key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
            all_employees_working_this_shift.append(shift_combinations[key])

        constraint_model.AddExactlyOne(all_employees_working_this_shift)


def add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar]) -> None:
    shift_grouping_func = lambda shift: shift.start_time.date()

    for _, shifts_group in itertools.groupby(shifts, shift_grouping_func):
        shifts_in_day = list(shifts_group)
        for employee in employees:
            works_shifts_on_day: list[IntVar] = []
            for shift in shifts_in_day:
                key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
                works_shifts_on_day.append(shift_combinations[key])

            constraint_model.AddAtMostOne(works_shifts_on_day)


def add_limit_employees_working_days_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar], max_working_days: int) -> None:
    for employee in employees:
        shifts_employee_is_working: list[IntVar] = []

        for shift in shifts:
            key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
            shifts_employee_is_working.append(shift_combinations[key])

        constraint_model.Add(sum(shifts_employee_is_working) <= max_working_days)


def add_minimum_time_between_closing_shift_and_next_shift_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar], min_hours_between_shifts: datetime.timedelta) -> None:
    for employee in employees:
        shifts_window = 3
        for shift1, shift2, shift3 in more_itertools.windowed(shifts, shifts_window):
            worked_closing_shift_yesterday = constraint_model.NewBoolVar(f"closing_{shift1.shift_id}_{employee.employee_id}")

            # if the shifts list contain less then a number that is divided by 'shifts_window',
            # more_itertools.windowed will fill in None.
            if shift2 and shift1.shift_type == ShiftTypesEnum.CLOSING:
                end_datetime_shift1 = shift1.end_time
                start_datetime_shift2 = shift2.start_time

                shift1_key = ShiftCombinationsKey(employee.employee_id, shift1.shift_id)
                constraint_model.Add(worked_closing_shift_yesterday == shift_combinations.get(shift1_key, 0))

                if start_datetime_shift2 - end_datetime_shift1 <= min_hours_between_shifts:
                    shift2_key = ShiftCombinationsKey(employee.employee_id, shift2.shift_id)
                    constraint_model.Add(shift_combinations[shift2_key] == 0).OnlyEnforceIf(worked_closing_shift_yesterday)

                if shift3:
                    start_datetime_shift3 = shift3.start_time

                    if start_datetime_shift3 - end_datetime_shift1 <= min_hours_between_shifts:
                        shift3_key = ShiftCombinationsKey(employee.employee_id, shift3.shift_id)
                        constraint_model.Add(shift_combinations[shift3_key] == 0).OnlyEnforceIf(worked_closing_shift_yesterday)
