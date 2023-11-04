from datetime import datetime

from ortools.sat.python import cp_model

from constraints_file import *
from models.employees.employee import Employee, EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_enum import ShiftTypesEnum


def generate_sun_to_sat_shifts(sun: int, sat: int, month: int, year: int, shifts):

    # datetime.weekday() will return an int representing: Monday is 0 and Sunday is 6

    for day in range(sun, sat + 1):
        # if the day is fri or sat
        if 3 < datetime(year, month, day).weekday() < 6:
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
            if datetime(year, month, day).weekday() == 3:
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

    cp_model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shift_this_week, cp_model)
    add_one_employee_per_shift_constraint(shift_this_week, employees, cp_model, all_shifts)
    add_at_most_one_shift_in_the_same_day_constraint(shift_this_week, employees, cp_model, all_shifts)
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, shift_this_week, employees, cp_model, all_shifts)
    add_no_morning_shift_after_closing_shift_constraint(shift_this_week, employees, cp_model, all_shifts)
    add_max_6_working_days_a_week_constraint(shift_this_week, employees, cp_model, all_shifts)
    objective_function(shift_this_week, employees, cp_model, all_shifts)


    print("Hello World!")
