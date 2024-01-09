import datetime
import itertools
import more_itertools

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar
from models.employees.employee import Employee
from models.employees.employee_status_enum import EmployeeStatusEnum
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


def add_minimum_time_between_closing_shift_and_next_shift_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar], min_time_between_shifts: datetime.timedelta) -> None:
    closing_shifts = [shift for shift in shifts if shift.shift_type == ShiftTypesEnum.CLOSING]

    for employee in employees:

        for closing_shift in closing_shifts:
            worked_closing_shift_yesterday = constraint_model.NewBoolVar(f"closing_{closing_shift.shift_id}_{employee.employee_id}")

            closing_shift_key = ShiftCombinationsKey(employee.employee_id, closing_shift.shift_id)
            # A variable for better visualization, this represents the assignment to
            # worked_closing_shift_yesterday BoolVar and not equality. If the IntVar is true (meaning the employee worked),
            # worked_closing_shift_yesterday will hold true, and vice versa.
            employee_assignment_closing_shift = worked_closing_shift_yesterday == shift_combinations[closing_shift_key]
            constraint_model.Add(employee_assignment_closing_shift)

            forbidden_shifts = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for shift in shifts if
                                shift.start_time > closing_shift.start_time and (shift.start_time - closing_shift.end_time) <= min_time_between_shifts]

            constraint_model.Add(sum(forbidden_shifts) == 0).OnlyEnforceIf(worked_closing_shift_yesterday)


def add_prevent_new_employees_from_working_parallel_shifts_together(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar], parallel_shift_types: list[ShiftTypesEnum]) -> None:
    shift_grouping_func = lambda shift: shift.start_time.date()

    for _, shifts_group in itertools.groupby(shifts, shift_grouping_func):
        shifts_in_day = list(shifts_group)
        new_emps_in_parallel_shifts: list[IntVar] = []
        for employee in employees:
            for shift in shifts_in_day:
                if employee.employee_status == EmployeeStatusEnum.new_employee and shift.shift_type in parallel_shift_types:

                    key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
                    new_emps_in_parallel_shifts.append(shift_combinations[key])

        constraint_model.AddAtMostOne(new_emps_in_parallel_shifts)
