from datetime import date
from typing import Dict, Tuple

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar
import datetime

from models.employees.employee import Employee
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.frozen_shift_combinations_key import FrozenShiftCombinationKey
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


# Returns a list of IntVar representing a true false of all the "new employees" that work each shift
def generate_new_employees_on_shift(employees: list[Employee], shifts: list[Shift], shift_combinations: dict[FrozenShiftCombinationKey, IntVar], shift_type: ShiftTypesEnum, day: datetime.date) -> \
list[IntVar]:
    employees_on_shift = []

    for employee in employees:
        for shift in shifts:

            start_date = shift.start_date_of_shift
            end_date = shift.end_date_of_shift

            if start_date == day and employee.status == EmployeeStatusEnum.new_employee and shift.shift_type.name_of_shift == shift_type:
                employees_on_shift.append(
                    shift_combinations[FrozenShiftCombinationKey(employee.id, start_date, end_date, shift_type)])

    return employees_on_shift


# Returns a dictionary that contains all the combinations of shifts and employees as: the employee id, start date
#       (as a datetime object) of the shift, end date ( also as a datetime object) of the shift, and the shift's type,
#       as a key, and the value will be an IntVar that will represent true or false based of if the employee is
#       working that shift or not.
def generate_shift_employee_combinations(employees: list[Employee], shifts: list[Shift], constraint_model: cp_model.CpModel) -> \
        dict[FrozenShiftCombinationKey, IntVar]:
    combinations = {}
    for employee in employees:
        employee_id = employee.id

        for shift in shifts:
            start_date = shift.end_date_of_shift
            end_date = shift.end_date_of_shift
            shift_type = shift.shift_type.name_of_shift

            combinations[FrozenShiftCombinationKey(employee_id, start_date, end_date, shift_type)] = constraint_model.NewBoolVar(
                    f"employee{employee_id}_start_date{start_date}_end_date{end_date}_shift{shift_type}")

    return combinations


def add_at_most_one_shift_for_employee_in_a_day_constrain(constraint_model: cp_model.CpModel, employees_assigned_shifts_in_a_day: list[IntVar]):
    constraint_model.AddAtMostOne(employees_assigned_shifts_in_a_day)


def add_at_least_one_employee_per_shift_constraint(constraint_model: cp_model.CpModel, employees_on_shift_shifts: list[IntVar]) -> None:
    constraint_model.AddExactlyOne(employees_on_shift_shifts)


def add_prevent_new_employees_working_together_constraint(first_shift: ShiftTypesEnum, second_shift: ShiftTypesEnum, constraint_model: cp_model.CpModel, new_employees_on_first_shift: list[IntVar], new_employees_on_second_shift: list[IntVar], day: datetime.date):
    condition_sift_1 = constraint_model.NewBoolVar(f"condition_shift_1_{day}_{first_shift}")
    condition_sift_2 = constraint_model.NewBoolVar(f"condition_shift_2_{day}_{second_shift}")

    constraint_model.Add(sum(new_employees_on_first_shift) >= 1).OnlyEnforceIf(condition_sift_1)
    constraint_model.Add(sum(new_employees_on_first_shift) == 0).OnlyEnforceIf(condition_sift_1.Not())

    constraint_model.Add(sum(new_employees_on_second_shift) >= 1).OnlyEnforceIf(condition_sift_2)
    constraint_model.Add(sum(new_employees_on_second_shift) == 0).OnlyEnforceIf(condition_sift_2.Not())

    constraint_model.AddBoolOr([condition_sift_1.Not(), condition_sift_2.Not()])


def add_max_working_days_a_week_constraint(employee_working_days: int, constraint_model: cp_model.CpModel, max_working_days: int):
    constraint_model.Add(employee_working_days <= max_working_days)


def add_no_morning_shift_after_closing_shift_constraint(employee: Employee, closing_shift: Shift, next_shift: Shift, shift_combinations: dict[FrozenShiftCombinationKey, IntVar], constraint_model: cp_model.CpModel):
    worked_closing_shift_yesterday = constraint_model.NewBoolVar(f"{employee.id}_worked_closing_shift_yesterday_day")

    constraint_model.Add(worked_closing_shift_yesterday == shift_combinations.get(FrozenShiftCombinationKey(employee.id, closing_shift.start_date_of_shift, closing_shift.end_date_of_shift, closing_shift.shift_type.name_of_shift), 0))

    constraint_model.Add(shift_combinations[FrozenShiftCombinationKey(employee.id, next_shift.start_date_of_shift, next_shift.end_date_of_shift, next_shift.shift_type.name_of_shift)] == 0).OnlyEnforceIf(
        worked_closing_shift_yesterday)
