import datetime
import itertools
import uuid
from typing import Tuple
from uuid import UUID

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
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


def add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar], min_time_between_shifts: datetime.timedelta, afternoon_start_time: datetime.time):
    all_afternoon_shifts = [shift for shift in shifts if afternoon_start_time <= shift.start_time.time()]

    for employee in employees:
        for afternoon_shift in all_afternoon_shifts:
            worked_an_afternoon_shift_yesterday = constraint_model.NewBoolVar(f"afternoon_{afternoon_shift.shift_id}_{employee.employee_id}")
            afternoon_shift_key = ShiftCombinationsKey(employee.employee_id, afternoon_shift.shift_id)
            employee_assignment_an_afternoon_shift = worked_an_afternoon_shift_yesterday == shift_combinations[afternoon_shift_key]

            constraint_model.Add(employee_assignment_an_afternoon_shift)

            forbidden_shifts = []

            for shift in shifts:
                if shift != afternoon_shift and shift not in forbidden_shifts:
                    time_between_shift_and_afternoon_shift = shift.start_time - afternoon_shift.end_time

                    if time_between_shift_and_afternoon_shift <= min_time_between_shifts:
                        forbidden_shifts.append(shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)])
            
            constraint_model.Add(sum(forbidden_shifts) == 0).OnlyEnforceIf(worked_an_afternoon_shift_yesterday)
            constraint_model.Add(sum(forbidden_shifts) > 0).OnlyEnforceIf(worked_an_afternoon_shift_yesterday.Not())


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
        shifts_without_shift = [s for s in shifts if s != shift]
        parallel_shifts_to_shift: list[Shift] = get_overlapping_shifts(shift, shifts_without_shift)
        parallel_shift_permutations: list[list[Shift]] = get_shift_permutations_from_shifts(parallel_shifts_to_shift)
        fully_overlapping_permutations: list[set[Shift]] = [set(permutation) for permutation in parallel_shift_permutations if is_fully_overlapping(shift, permutation)]
        hermetic_non_supersets_permutations: list[set[Shift]] = get_permutations_without_supersets(fully_overlapping_permutations)  # Non-supersets
        for perm in hermetic_non_supersets_permutations:
            add_values_to_fully_non_new_emps_in_all_shift_permutations(perm, fully_non_new_emps_in_all_shift_permutations, constraint_model, non_new_emps_in_each_shifts)
        non_new_emps_in_shift_permutations: dict[str, IntVar] = get_non_new_emps_in_shift_permutations(fully_non_new_emps_in_all_shift_permutations, hermetic_non_supersets_permutations)

        non_new_emps_in_shift_permutations_id = ','.join(non_new_emps_in_shift_permutations.keys())
        any_of_the_perms_are_true = constraint_model.NewBoolVar(f"any_perm_{non_new_emps_in_shift_permutations_id}")
        all_perms = fully_non_new_emps_in_all_shift_permutations.values()
        not_perms = [perm.Not() for perm in all_perms]
        constraint_model.AddBoolOr(all_perms).OnlyEnforceIf(any_of_the_perms_are_true)
        constraint_model.AddBoolAnd(not_perms).OnlyEnforceIf(any_of_the_perms_are_true.Not())
        any_of_the_perms_are_true_for_each_shift[non_new_emps_in_shift_permutations_id] = any_of_the_perms_are_true

        # Only if one of the permutations are worked by non-new employees, a new employee can work shift.
        new_employees_works_this_shift = new_emps_in_each_shifts[shift.shift_id]
        not_non_new_emp_in_perm = [non_new_emp_in_perm.Not() for non_new_emp_in_perm in non_new_emps_in_shift_permutations.values()]
        constraint_model.AddBoolOr(non_new_emps_in_shift_permutations.values()).OnlyEnforceIf(new_employees_works_this_shift)
        constraint_model.AddBoolAnd(not_non_new_emp_in_perm).OnlyEnforceIf(new_employees_works_this_shift.Not())

    return new_emps_in_each_shifts, non_new_emps_in_each_shifts, fully_non_new_emps_in_all_shift_permutations, any_of_the_perms_are_true_for_each_shift


def is_fully_overlapping(comparison_shift, overlapping_shifts: list['Shift']):
    shifts_sorted_by_start_time = sorted(overlapping_shifts, key=lambda shift: shift.start_time)
    shifts_start_time_end_time_range: list['Shift'] = [shifts_sorted_by_start_time[0]]

    for shift_perm in shifts_sorted_by_start_time[1:]:
        shift_start_during_prev_one = shift_perm.start_time <= shifts_start_time_end_time_range[-1].end_time

        if not shift_start_during_prev_one:
            return False
        shifts_start_time_end_time_range.append(shift_perm)
    first_shift_starts_before_shift_starts = shifts_start_time_end_time_range[0].start_time <= comparison_shift.start_time
    last_shift_ends_after_shift_ends = shifts_start_time_end_time_range[-1].end_time >= comparison_shift.end_time

    return first_shift_starts_before_shift_starts and last_shift_ends_after_shift_ends


def add_values_to_fully_non_new_emps_in_all_shift_permutations(shifts: set[Shift], fully_non_new_emps_in_all_shift_permutations: dict[str, IntVar], constraint_model: cp_model.CpModel, non_new_employees_in_shifts: dict[uuid.UUID, IntVar]):
    permutation_id = get_permutation_id(shifts)
    if permutation_id not in fully_non_new_emps_in_all_shift_permutations:
        non_new_employees_work_perm = constraint_model.NewBoolVar(f"fully_non_new_emps_{permutation_id}")
        non_new_emps_in_perm = [non_new_employees_in_shifts[shift.shift_id] for shift in shifts]
        not_non_new_emp_in_shift = [non_new_emp_in_shift.Not() for non_new_emp_in_shift in non_new_emps_in_perm]

        constraint_model.AddBoolAnd(non_new_emps_in_perm).OnlyEnforceIf(non_new_employees_work_perm)
        constraint_model.AddBoolOr(not_non_new_emp_in_shift).OnlyEnforceIf(non_new_employees_work_perm.Not())
        fully_non_new_emps_in_all_shift_permutations[permutation_id] = non_new_employees_work_perm


def get_non_new_emps_in_shift_permutations(non_new_emps_in_all_permutations: dict[str, IntVar], permutations: list[set[Shift]]) -> dict[str, IntVar]:
    non_new_emps_in_shift_permutations: dict[str, IntVar] = {}

    for shifts_permutation in permutations:
        permutation_id = get_permutation_id(shifts_permutation)
        non_new_emps_in_shift_permutations[permutation_id] = non_new_emps_in_all_permutations[permutation_id]

    return non_new_emps_in_shift_permutations


def get_permutations_without_supersets(fully_overlapping_permutations: list[set[Shift]]) -> list[set[Shift]]:
    super_perms: list[set[Shift]] = []
    for overlapping_permutation in fully_overlapping_permutations:
        if overlapping_permutation in super_perms:
            continue
        else:
            for other_overlapping_permutation in fully_overlapping_permutations:
                if overlapping_permutation != other_overlapping_permutation and other_overlapping_permutation.issuperset(overlapping_permutation):
                    super_perms.append(other_overlapping_permutation)

    # Sets are not hashable because they are mutable. Converting these lists to frozensets allows me to use the "-"
    # operator, because then these lists are immutable and hashable.
    frozenset_fully_overlapping_permutations = {frozenset(perm) for perm in fully_overlapping_permutations}
    frozenset_super_perms = {frozenset(perm) for perm in super_perms}

    perfect_overlapping_permutations = list(frozenset_fully_overlapping_permutations - frozenset_super_perms)
    return perfect_overlapping_permutations


def get_overlapping_shifts(shift: Shift, shifts: list[Shift]) -> list[Shift]:
    overlapping_shifts_to_shift: list[Shift] = []
    for comparison_shift in shifts:
        if shift.overlaps_with(comparison_shift):
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


def add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar]) -> list[IntVar]:
    deviations = []
    for employee in employees:
        emp_shifts = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for shift in shifts]
        deviation = constraint_model.NewIntVar(0, len(emp_shifts), f'deviation_{employee.employee_id}')
        multy_deviation = constraint_model.NewIntVar(0, pow(len(emp_shifts), 2), f'multy_deviation_{employee.employee_id}')

        constraint_model.AddAbsEquality(deviation, sum(emp_shifts) - employee.position.value)
        constraint_model.AddMultiplicationEquality(multy_deviation, deviation, deviation)
        deviations.append(multy_deviation)
    constraint_model.Minimize(sum(deviations))
    return deviations


def add_aspire_to_maximize_all_employees_preferences_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar]):
    for employee in employees:
        for day_cannot_work in employee.preferences.days_cannot_work:
            shifts_cannot_work = [shift for shift in shifts if shift.start_time.date() == day_cannot_work.day_date]
            for shift_cannot_work in shifts_cannot_work:
                constraint_model.Add(shift_combinations[ShiftCombinationsKey(employee.employee_id, shift_cannot_work.shift_id)] == 0)

        for emp_shift_preference in employee.preferences.shifts_prefer_to_work_in_days:
            shifts_prefer_to_work_in_day = [shift for shift in shifts if shift.shift_type in emp_shift_preference.shifts and shift.start_time.date() == emp_shift_preference.day_date]

            employee_shift_preferences = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for shift in shifts_prefer_to_work_in_day]
            constraint_model.Maximize(sum(employee_shift_preferences))

        for emp_shift_cannot_work_preference in employee.preferences.shifts_cannot_work:
            shifts_cannot_work_in_day = [shift for shift in shifts if shift.shift_type in emp_shift_cannot_work_preference.shifts and shift.start_time.date() == emp_shift_cannot_work_preference.day_date]

            employee_shift_preferences = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for shift in shifts_cannot_work_in_day]
            constraint_model.Add(sum(employee_shift_preferences) == 0)

        for day_prefer_not_to_work in employee.preferences.days_prefer_not_to_work:
            shifts_prefer_not_to_work = [shift for shift in shifts if shift.start_time.date() == day_prefer_not_to_work.day_date]
            shift_assignments = [shift_combinations[ShiftCombinationsKey(employee.employee_id, shift.shift_id)] for shift in shifts_prefer_not_to_work]

            constraint_model.Minimize(sum(shift_assignments))

        for shift_emp_has_to_work in employee.preferences.shifts_has_to_work_in_days:
            shifts_has_to_work = [shift for shift in shifts if shift.shift_type in shift_emp_has_to_work.shifts and shift.start_time.date() == shift_emp_has_to_work.day_date]
            for shift in shifts_has_to_work:
                key = ShiftCombinationsKey(employee.employee_id, shift.shift_id)
                constraint_model.Add(shift_combinations[key] == 1)


def add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts: list[Shift], employees: list[Employee], constraint_model: cp_model.CpModel, shift_combinations: dict[ShiftCombinationsKey, IntVar]):
    for emp in employees:
        shifts_cannot_work = [shift for shift in shifts if shift.shift_type not in emp.shift_types_trained_to_do]

        for shift in shifts_cannot_work:
            key = ShiftCombinationsKey(emp.employee_id, shift.shift_id)
            constraint_model.Add(shift_combinations[key] == 0)
