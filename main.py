from datetime import datetime

from ortools.sat.python import cp_model

from constraints_file import *
from models.days_enum import DaysEnum
from models.employees.employee import Employee, EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_enum import ShiftTypesEnum
from models.shifts.shifts_times import ShiftTimes


# A function to generate the shifts from sunday to saturday
def generate_sun_to_sat_shifts(sun_day: int, sat_day: int, month: int, year: int, shifts):

    for day in range(sun_day, sat_day + 1):
        # if the day is fri or sat
        if DaysEnum.THU.value < datetime(year, month, day).weekday() <= DaysEnum.SAT.value:
            # could do variables for each shift start and end datetime objects to make these lines shorter,
            # but then there will be a lot of variables..
            shifts.append(Shift(ShiftTypesEnum.WEEKEND_MORNING,
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_morning_shift_time.value["start"]),
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_morning_shift_time.value["end"])))

            shifts.append(Shift(ShiftTypesEnum.WEEKEND_MORNING_BACKUP,
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_backup_shift_times.value["start"]),
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_backup_shift_times.value["end"])))

            shifts.append(Shift(ShiftTypesEnum.EVENING,
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_evening_shift_times.value["start"]),
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_evening_shift_times.value["end"])))

            shifts.append(Shift(ShiftTypesEnum.CLOSING,
                                datetime.combine(datetime(year, month, day), ShiftTimes.weekend_closing_shift_times.value["start"]),
                                datetime.combine(datetime(year, month, day+1), ShiftTimes.weekend_closing_shift_times.value["end"])))

        # sun to thu
        else:
            shifts.append(Shift(ShiftTypesEnum.MORNING,
                                datetime.combine(datetime(year, month, day), ShiftTimes.morning_shift_times.value["start"]),
                                datetime.combine(datetime(year, month, day), ShiftTimes.morning_shift_times.value["end"])))

            shifts.append(Shift(ShiftTypesEnum.EVENING,
                                datetime.combine(datetime(year, month, day), ShiftTimes.evening_shift_times.value["start"]),
                                datetime.combine(datetime(year, month, day), ShiftTimes.evening_shift_times.value["end"])))

            # if the day is thu
            if datetime(year, month, day).weekday() == DaysEnum.THU.value:
                shifts.append(Shift(ShiftTypesEnum.THURSDAY_BACKUP,
                                    datetime.combine(datetime(year, month, day), ShiftTimes.thu_backup_shift_times.value["start"]),
                                    datetime.combine(datetime(year, month, day), ShiftTimes.thu_backup_shift_times.value["end"])))

                shifts.append(Shift(ShiftTypesEnum.CLOSING,
                                    datetime.combine(datetime(year, month, day), ShiftTimes.thu_closing_shift_times.value["start"]),
                                    datetime.combine(datetime(year, month, day+1), ShiftTimes.thu_closing_shift_times.value["end"])))
            else:
                shifts.append(Shift(ShiftTypesEnum.CLOSING,
                                    datetime.combine(datetime(year, month, day), ShiftTimes.closing_shift_times.value["start"]),
                                    datetime.combine(datetime(year, month, day+1), ShiftTimes.closing_shift_times.value["end"])))


if __name__ == "__main__":
    shift_this_week = []

    generate_sun_to_sat_shifts(15, 21, 10, 2023, shift_this_week)

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
        print(f"{pair[shift_index].type.value} shift, starts at {pair[shift_index].start_date_and_time_of_shift}, ends at {pair[shift_index].end_date_and_time_of_shift}, worked by {pair[employee_index].name}")
        if pair[shift_index].type == ShiftTypesEnum.CLOSING:
            print()
