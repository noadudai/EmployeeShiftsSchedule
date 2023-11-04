from datetime import datetime

from ortools.sat.python import cp_model

from constraints_file import *
from models.days_enum import DaysEnum
from models.employees.employee import Employee, EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_enum import ShiftTypesEnum


def generate_sun_to_sat_shifts(sun: int, sat: int, month: int, year: int, shifts):

    # datetime.weekday() will return an int representing: Monday is 0 and Sunday is 6

    for day in range(sun, sat + 1):
        # if the day is fri or sat
        if DaysEnum.THU.value < datetime(year, month, day).weekday() < DaysEnum.SAT.value:
            shifts.append(Shift(ShiftTypesEnum.WEEKEND_MORNING, datetime(year, month, day, 9, 15), datetime(year, month, day, 18)))
            shifts.append(Shift(ShiftTypesEnum.WEEKEND_MORNING_BACKUP, datetime(year, month, day, 12),
                                datetime(year, month, day, 18)))
            shifts.append(Shift(ShiftTypesEnum.EVENING, datetime(year, month, day, 18), datetime(year, month, day, 22)))
            shifts.append(Shift(ShiftTypesEnum.CLOSING, datetime(year, month, day, 21, 30), datetime(year, month, day + 1, 2)))

        # sun to thu
        else:
            shifts.append(Shift(ShiftTypesEnum.MORNING, datetime(year, month, day, 10), datetime(year, month, day, 16)))
            shifts.append(Shift(ShiftTypesEnum.EVENING, datetime(year, month, day, 16), datetime(year, month, day, 22)))

            # if the day is thu
            if datetime(year, month, day).weekday() == DaysEnum.THU.value:
                shifts.append(Shift(ShiftTypesEnum.THURSDAY_BACKUP, datetime(year, month, day, 19, 30),
                                    datetime(year, month, day + 1, 0, 0, 0)))
                shifts.append(Shift(ShiftTypesEnum.CLOSING, datetime(year, month, day, 21, 30),
                                    datetime(year, month, day + 1, 2)))
            else:
                shifts.append(Shift(ShiftTypesEnum.CLOSING, datetime(year, month, day, 19, 30), datetime(year, month, day + 1, 2)))


if __name__ == "__main__":
    shift_this_week = []

    generate_sun_to_sat_shifts(15, 21, 10, 2023, shift_this_week)

    # If I am removing one employee (leaving only 2 employees), there is no optimal solution because of the constraint
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

    for shift in schedule.week_schedule:
        print(f"{shift.type.value} in date {shift.get_str_start_date_from_shift()}, is worked by {shift.employee.name}")
