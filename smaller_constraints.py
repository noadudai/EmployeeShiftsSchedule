from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar
import datetime

from models.employees.employee import Employee
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


def add_at_most_one_employee_per_shift_constrain(constraint_model: cp_model.CpModel, worker_shifts_worked_on_a_day: list[IntVar]):
    constraint_model.AddAtMostOne(worker_shifts_worked_on_a_day)


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


def add_no_morning_shift_after_closing_shift_constraint(employee: Employee, closing_shift: Shift, next_shift: Shift, shift_combinations: dict[tuple[int, str, str, ShiftTypesEnum], IntVar], constraint_model: cp_model.CpModel):
    worked_closing_shift_yesterday = constraint_model.NewBoolVar(f"{employee.id}_worked_closing_shift_yesterday_day")

    constraint_model.Add(worked_closing_shift_yesterday == shift_combinations.get((employee.id, closing_shift.get_str_start_date(), closing_shift.get_str_end_date(), closing_shift.shift_type.name_of_shift), 0))

    constraint_model.Add(shift_combinations[(employee.id, next_shift.get_str_start_date(), next_shift.get_str_end_date(), next_shift.shift_type.name_of_shift)] == 0).OnlyEnforceIf(
        worked_closing_shift_yesterday)
