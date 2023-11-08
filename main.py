import datetime

from ortools.sat.python import cp_model

from constraints_file import *
from models.days_enum import DaysEnum
from models.employees.employee import Employee, EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.shifts.shifts_times import ShiftTimes
from models.shifts.shift_type import ShiftType


# A function to generate the shifts from sunday to saturday
def generate_sun_to_sat_shifts_for_test(sunday: datetime.date, saturday: datetime.date, shifts):
    day = sunday

    # these times are for testing.
    morning_shift = ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0))
    evening_shift = ShiftType(ShiftTypesEnum.EVENING, datetime.time(17, 0), datetime.time(22, 0))
    closing_shift = ShiftType(ShiftTypesEnum.CLOSING, datetime.time(19, 30), datetime.time(2, 0))
    thu_backup_shift = ShiftType(ShiftTypesEnum.THURSDAY_BACKUP, datetime.time(19, 30), datetime.time(22, 0))
    thu_closing_shift = ShiftType(ShiftTypesEnum.CLOSING, datetime.time(21, 0), datetime.time(2, 0))
    weekend_morning_shift = ShiftType(ShiftTypesEnum.WEEKEND_MORNING, datetime.time(9, 15), datetime.time(18, 0))
    weekend_backup_shift = ShiftType(ShiftTypesEnum.WEEKEND_MORNING_BACKUP, datetime.time(12, 0), datetime.time(18, 0))
    weekend_evening_shift = ShiftType(ShiftTypesEnum.EVENING, datetime.time(18, 0), datetime.time(22, 0))

    delta = datetime.timedelta(days=1)

    while day <= saturday:
        if DaysEnum.THU.value < day.weekday() <= DaysEnum.SAT.value:
            shifts.append(Shift(weekend_morning_shift, day, day))
            shifts.append(Shift(weekend_backup_shift, day, day))
            shifts.append(Shift(weekend_evening_shift, day, day))
            shifts.append(Shift(closing_shift, day, day + delta))

        # sun to thu
        else:
            shifts.append(Shift(morning_shift, day, day))
            shifts.append(Shift(evening_shift, day, day))

            # if the day is thu
            if day.weekday() == DaysEnum.THU.value:
                shifts.append(Shift(thu_backup_shift, day, day))
                shifts.append(Shift(thu_closing_shift, day, day + delta))
            else:
                shifts.append(Shift(closing_shift, day, day + delta))

        day += delta


if __name__ == "__main__":
    shift_this_week = []

    generate_sun_to_sat_shifts_for_test(datetime.date(2023, 11, 5), datetime.date(2023, 11, 11), shift_this_week)

    # If I am leaving only 2 employees, there is no optimal solution because of the constraint
    # that prevents an employee to work more than one shift that starts on the same day.

    employee1 = Employee("Emily", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    employee2 = Employee("John", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 2)
    employee3 = Employee("Michael", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 3)
    employee4 = Employee("William", EmployeePriorityEnum.MEDIUM, EmployeeStatusEnum.senior_employee, 4)
    employee5 = Employee("Dow", EmployeePriorityEnum.MEDIUM, EmployeeStatusEnum.junior_employee, 5)

    employees = [employee1, employee2, employee3, employee4, employee5]

    max_working_days_in_a_week = 6

    cp_model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shift_this_week, cp_model)
    add_one_employee_per_shift_constraint(shift_this_week, employees, cp_model, all_shifts)
    add_at_most_one_shift_in_the_same_day_constraint(shift_this_week, employees, cp_model, all_shifts)
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, shift_this_week, employees, cp_model, all_shifts)
    add_no_morning_shift_after_closing_shift_constraint(shift_this_week, employees, cp_model, all_shifts)
    add_max_working_days_a_week_constraint(shift_this_week, employees, cp_model, all_shifts, max_working_days_in_a_week)
    schedule = create_optimal_schedule(shift_this_week, employees, cp_model, all_shifts)

    for pair in schedule.week_schedule:
        shift_index = 0
        employee_index = 1
        print(f"{pair[shift_index].shift_type.name_of_shift.value} shift, starts at {pair[shift_index].start_date_of_shift}, ends at {pair[shift_index].end_date_of_shift}, worked by {pair[employee_index].name}")
        if pair[shift_index].shift_type == ShiftTypesEnum.CLOSING:
            print()
