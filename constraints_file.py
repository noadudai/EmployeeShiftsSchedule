import datetime
import itertools
import uuid
from typing import Tuple, Dict
from uuid import UUID

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


def add_prevent_new_employees_from_working_parallel_shifts_together(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar])-> \
tuple[dict[UUID, IntVar], dict[UUID, IntVar], dict[str, IntVar], dict[str, IntVar]]:

    new_emps_in_each_shifts: dict[uuid.UUID, IntVar] = {}
    non_new_emps_in_each_shifts: dict[uuid.UUID, IntVar] = {}
    fully_non_new_emps_in_all_shift_permutations: dict[str, IntVar] = {}
    any_of_the_perms_are_true_for_each_shift: dict[str, IntVar] = {}

    for shift in shifts:
        # Set the values for new_emps_in_each_shifts and non_new_emps_in_each_shifts for each shift.
        new_emps_work_shift = constraint_model.NewBoolVar(f"new_emps_{shift.shift_id}")
        new_emps_in_shifts = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for employee in employees if employee.employee_status == EmployeeStatusEnum.new_employee]
        not_new_emps_in_shift = [new_emp_in_shift.Not() for new_emp_in_shift in new_emps_in_shifts]

        constraint_model.AddBoolOr(new_emps_in_shifts).OnlyEnforceIf(new_emps_work_shift)
        constraint_model.AddBoolAnd(not_new_emps_in_shift).OnlyEnforceIf(new_emps_work_shift.Not())
        new_emps_in_each_shifts[shift.shift_id] = new_emps_work_shift

        non_new_emps_work_shift = constraint_model.NewBoolVar(f"non_new_emps_{shift.shift_id}")
        non_new_emps_in_shifts = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for employee in employees if employee.employee_status != EmployeeStatusEnum.new_employee]
        not_non_new_emps_in_shifts = [non_new_emp_in_shift.Not() for non_new_emp_in_shift in non_new_emps_in_shifts]

        constraint_model.AddBoolOr(non_new_emps_in_shifts).OnlyEnforceIf(non_new_emps_work_shift)
        constraint_model.AddBoolAnd(not_non_new_emps_in_shifts).OnlyEnforceIf(non_new_emps_work_shift.Not())
        non_new_emps_in_each_shifts[shift.shift_id] = non_new_emps_work_shift

    for shift in shifts:
        parallel_shifts_to_shift: list[Shift] = get_overlapping_shifts(shift, shifts)
        parallel_shift_permutations: list[list[Shift]] = get_shift_permutations_from_shifts(parallel_shifts_to_shift)
        fully_overlapping_permutations: list[set[Shift]] = [set(permutation) for permutation in parallel_shift_permutations if is_fully_overlapping(shift, permutation)]
        hermetic_non_supersets_permutations: list[set[Shift]] = get_permutations_without_supersets(fully_overlapping_permutations)  # Non-supersets
        non_new_emps_in_shift_permutations: dict[str, IntVar] = get_non_new_emps_in_shift_permutations(constraint_model, non_new_emps_in_each_shifts, fully_non_new_emps_in_all_shift_permutations, hermetic_non_supersets_permutations)

        non_new_emps_in_shift_permutations_id = ','.join(non_new_emps_in_shift_permutations.keys())
        any_of_the_perms_are_true = constraint_model.NewBoolVar(f"any_perm_{non_new_emps_in_shift_permutations_id}")
        all_perms = fully_non_new_emps_in_all_shift_permutations.values()
        not_perms = [perm.Not() for perm in all_perms]
        constraint_model.AddAtLeastOne(all_perms).OnlyEnforceIf(any_of_the_perms_are_true)
        constraint_model.AddBoolAnd(not_perms).OnlyEnforceIf(any_of_the_perms_are_true.Not())
        any_of_the_perms_are_true_for_each_shift[non_new_emps_in_shift_permutations_id] = any_of_the_perms_are_true

        # Only if one of the permutations are worked by non-new employees, a new employee can work shift.
        new_employees_works_this_shift = new_emps_in_each_shifts[shift.shift_id]
        not_non_new_emp_in_perm = [non_new_emp_in_perm.Not() for non_new_emp_in_perm in non_new_emps_in_shift_permutations.values()]
        constraint_model.AddBoolOr(non_new_emps_in_shift_permutations.values()).OnlyEnforceIf(new_employees_works_this_shift)
        constraint_model.AddBoolAnd(not_non_new_emp_in_perm).OnlyEnforceIf(new_employees_works_this_shift.Not())

    return new_emps_in_each_shifts, non_new_emps_in_each_shifts, fully_non_new_emps_in_all_shift_permutations, any_of_the_perms_are_true_for_each_shift


def is_fully_overlapping(shift, overlapping_shifts: list['Shift']):
    shifts_start_time_end_time_range: list['Shift'] = [overlapping_shifts[0]]
    for shift_perm in overlapping_shifts:
        if shifts_start_time_end_time_range[-1] != shift_perm and shift_perm.start_time <= shifts_start_time_end_time_range[-1].end_time:
            shifts_start_time_end_time_range.append(shift_perm)
        elif shift_perm.start_time > shifts_start_time_end_time_range[-1].end_time:
            return False
    if shifts_start_time_end_time_range[0].start_time <= shift.start_time and shifts_start_time_end_time_range[-1].end_time >= shift.end_time:
        return True
    else:
        return False


def get_non_new_emps_in_shift_permutations(constraint_model: cp_model.CpModel, non_new_employees_in_shifts: dict[uuid.UUID, IntVar], non_new_emps_in_all_permutations: dict[str, IntVar], overlapping_permutations: list[set[Shift]]) -> dict[str, IntVar]:
    non_new_emps_in_shift_permutations: dict[str, IntVar] = {}

    for shifts_permutation in overlapping_permutations:
        permutation_id = get_permutation_id(shifts_permutation)

        if permutation_id not in non_new_emps_in_all_permutations:
            non_new_employees_work_perm = constraint_model.NewBoolVar(f"fully_non_new_emps_{permutation_id}")
            non_new_emps_in_perm = [non_new_employees_in_shifts[shift_in_perm.shift_id] for shift_in_perm in shifts_permutation]
            not_non_new_emp_in_shift = [non_new_emp_in_shift.Not() for non_new_emp_in_shift in non_new_emps_in_perm]

            constraint_model.AddBoolAnd(non_new_emps_in_perm).OnlyEnforceIf(non_new_employees_work_perm)
            constraint_model.AddBoolOr(not_non_new_emp_in_shift).OnlyEnforceIf(non_new_employees_work_perm.Not())
            non_new_emps_in_all_permutations[permutation_id] = non_new_employees_work_perm
        else:
            non_new_employees_work_perm = non_new_emps_in_all_permutations[permutation_id]
        non_new_emps_in_shift_permutations[permutation_id] = non_new_employees_work_perm

    return non_new_emps_in_shift_permutations


def get_permutations_without_supersets(fully_overlapping_permutations: list[set[Shift]]):
    super_perms: list[set[Shift]] = []
    for overlapping_permutation in fully_overlapping_permutations:
        if overlapping_permutation in super_perms:
            continue
        else:
            for other_overlapping_permutation in fully_overlapping_permutations:
                if overlapping_permutation != other_overlapping_permutation and other_overlapping_permutation.issuperset(overlapping_permutation):
                    super_perms.append(other_overlapping_permutation)

    perfect_overlapping_permutations: list[set[Shift]] = [perm for perm in fully_overlapping_permutations if perm not in super_perms]
    return perfect_overlapping_permutations


def get_overlapping_shifts(shift: Shift, shifts: list[Shift]) -> list[Shift]:
    overlapping_shifts_to_shift: list[Shift] = []
    for comparison_shift in shifts:
        if comparison_shift != shift and shift.overlaps_with(comparison_shift):
            overlapping_shifts_to_shift.append(comparison_shift)
    return overlapping_shifts_to_shift


def get_shift_permutations_from_shifts(parallel_shifts: list[Shift]) -> list[list[Shift]]:
    permutations_lists: list[list[Shift]] = []

    for permutation_size in range(1, len(parallel_shifts) + 1):
        p: Tuple[Shift]
        permutations = [list(p) for p in itertools.permutations(parallel_shifts, permutation_size)]

        for permutation in permutations:
            permutations_lists.append(permutation)

    return permutations_lists


def get_permutation_id(shifts: set[Shift]) -> str:
    # UUID is not lexicographically sortable
    shifts_sorted_by_id = sorted(shifts, key= lambda shift: str(shift.shift_id))
    return f"perm_{''.join([str(shift.shift_id) for shift in shifts_sorted_by_id])}"


def add_prevent_overlapping_shifts_for_employees_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar]) -> None:
    for employee in employees:
        seen_shifts = []
        for shift in shifts:
            overlapping_shifts_for_employee: list[IntVar] = []
            for comparison_shift in shifts:
                if shift.overlaps_with(comparison_shift) and comparison_shift not in seen_shifts:
                    key = ShiftCombinationsKey(employee.employee_id, comparison_shift.shift_id)
                    overlapping_shifts_for_employee.append(shift_combinations[key])
                    seen_shifts.append(shift)
            constraint_model.AddAtMostOne(overlapping_shifts_for_employee)
