import datetime
import random
import pytest
from ortools.sat.python import cp_model

from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum
from constraints_file import is_fully_overlapping


def test_shifts_are_parallel_to_each_other():
    main_shift_start_time = datetime.datetime(2023, 12, 12, 9)

    main_shift = Shift("main_shitf", shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=main_shift_start_time + datetime.timedelta(hours=4))
    support_shift1 = Shift("support_shift1", shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=main_shift_start_time + datetime.timedelta(hours=2))
    support_shift2 = Shift("support_shift2", shift_type=ShiftTypesEnum.MORNING, start_time=support_shift1.end_time, end_time=main_shift.end_time)
    support_shift3 = Shift("support_shift3", shift_type=ShiftTypesEnum.MORNING, start_time=main_shift_start_time, end_time=support_shift1.end_time)

    assert(False == is_fully_overlapping(main_shift, [support_shift2]))
    assert(False == is_fully_overlapping(main_shift, [support_shift1]))
    assert(False == is_fully_overlapping(main_shift,[support_shift3]))
    assert(True == is_fully_overlapping(main_shift, [support_shift1, support_shift2]))
    assert(True == is_fully_overlapping(main_shift, [support_shift3, support_shift2]))
    assert(False == is_fully_overlapping(main_shift, [support_shift3, support_shift1]))
    assert(True == is_fully_overlapping(main_shift, [support_shift1, support_shift3, support_shift2]))


def test_overlapping_shifts_where_shift_starts_in_the_same_time():
    """
    [ A ]
    [ B   ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a.end_time + shift_duration)

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)

    pass


def test_overlapping_shifts_where_shift_ends_in_the_same_time():
    """
      [ A ]
    [ B   ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time - shift_duration, end_time=shift_a.end_time)

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shift_starts_before_other_shift_and_ends_before_other_shift_ends():
    """
    [ A ]
      [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time + (shift_duration / 2), end_time=shift_a.end_time + (shift_duration / 2))

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shift_starts_after_other_shift_starts_and_ends_after_other_shift_ends():
    """
      [ A ]
    [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a_start_time - (shift_duration / 2), end_time=shift_a.end_time - (shift_duration / 2))

    assert shift_a.overlaps_with(shift_b)
    assert shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_other_shift_starts_when_shift_ends():
    """
    [ A ]
        [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a.end_time, end_time=shift_a.end_time + shift_duration)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shift_starts_when_other_shift_ends():
    """
        [ A ]
    [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 12)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a.start_time - shift_duration, end_time=shift_a.start_time)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def test_overlapping_shifts_where_shifts_dont_overlap_at_all():
    """
    [ A ]
           [ B ]
    """
    shift_a_start_time = datetime.datetime(2024, 1, 1, 9)
    shift_duration = datetime.timedelta(hours=random.random())
    shift_a = Shift("shift_a", ShiftTypesEnum.MORNING, shift_a_start_time, end_time=shift_a_start_time + shift_duration)
    shift_b = Shift("shift_b", ShiftTypesEnum.MORNING, shift_a.end_time + shift_duration, end_time=shift_a.end_time + shift_duration + shift_duration)

    assert not shift_a.overlaps_with(shift_b)
    assert not shift_b.overlaps_with(shift_a)


def get_employees_shifts_assignments(all_shifts, employees, shifts, solver):
    emp_shift_assignments = {}
    for employee in employees:
        emp_shifts = []
        for shift in shifts:
            emp_assignment = all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]
            if solver.Value(emp_assignment):
                emp_shifts.append(solver.Value(emp_assignment))
        emp_shift_assignments[employee.employee_id] = emp_shifts
    return emp_shift_assignments
