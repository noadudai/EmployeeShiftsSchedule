import os
import uuid

from ortools.sat.python import cp_model
import pandas as pd

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint
from models.employees.employee import Employee
from models.employees.employees_file import all_employees
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_file import all_shifts_in_the_week
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.solution.one_schedule_solution_metadata import ScheduleSolution


def schedule_to_json(schedule: dict[uuid.uuid4, uuid.uuid4], shifts: list[Shift], employees: list[Employee]) -> dict:
    new_schedule_dict: dict[Shift, Employee] = {}

    for shift_id, emp_id in schedule.items():
        [shift_working] = [shift for shift in shifts if shift.shift_id == shift_id]
        [emp_working] = [emp for emp in employees if emp.employee_id == emp_id]
        new_schedule_dict[shift_working] = emp_working

    shift_index = 0
    sorted_schedule = sorted(new_schedule_dict.items(), key=lambda shift_emp_pair: shift_emp_pair[shift_index].start_time)

    dates = [shift.start_time.date() for shift in shifts]
    unique_dates = sorted(set(str(date) for date in dates))

    shift_types = [ShiftTypesEnum.MORNING.value, ShiftTypesEnum.MORNING_BACKUP.value,
                   ShiftTypesEnum.WEEKEND_MORNING_BACKUP.value, ShiftTypesEnum.EVENING.value,
                   ShiftTypesEnum.THURSDAY_BACKUP.value,
                   ShiftTypesEnum.WEEKEND_EVENING_BACKUP.value, ShiftTypesEnum.CLOSING.value]

    data_frame = pd.DataFrame(index=shift_types, columns=unique_dates)

    for shift_working, emp_working in sorted_schedule:

        frame = ShiftTypesEnum.MORNING.value if shift_working.shift_type == ShiftTypesEnum.WEEKEND_MORNING else shift_working.shift_type.value

        emp_and_shift_times_str = f"{emp_working.name} {str(shift_working.start_time.time())} - {str(shift_working.end_time.time())}"
        data_frame.at[frame, str(shift_working.start_time.date())] = emp_and_shift_times_str

    data_frame.fillna("", inplace=True)
    json_table = data_frame.to_dict()

    return json_table
