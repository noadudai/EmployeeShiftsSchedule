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
        employee_id = employee.id

        for shift in shifts:
            key = FrozenShiftCombinationsKey(employee_id, shift.shift_id)

            shift_combinations[key] = constraint_model.NewBoolVar(f"employee_{employee_id}_shift_{shift.shift_id}")

    return shift_combinations


# A constraint that ensures that there will be only one employee in each shift per day
def add_at_least_one_employee_per_shift_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[FrozenShiftCombinationsKey, IntVar]) -> None:
    for shift in shifts:

        constraint_model.AddExactlyOne(shift_combinations[FrozenShiftCombinationsKey(employee.id, shift.shift_id)] for employee in employees)
