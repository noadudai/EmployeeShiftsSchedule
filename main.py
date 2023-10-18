from datetime import datetime

from ortools.sat.python import cp_model

from models.employees.employee import Employee, EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_enum import ShiftTypesEnum
from models.constraints import Constraints


def test():
    # If I am removing one employee (leaving only 2 employees), there is no optimal solution because of the constraint
    # that prevents an employee to work more that one shift that starts on the same day.
    shift_morning_sun = Shift(ShiftTypesEnum.MORNING, datetime(2023, 10, 15, 10), datetime(2023, 10, 15, 16))
    shift_evening_sun = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 15, 16), datetime(2023, 10, 15, 22))
    shift_closing_sun = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 15, 19, 30), datetime(2023, 10, 16, 2))

    shift_morning_mon = Shift(ShiftTypesEnum.MORNING, datetime(2023, 10, 16, 10), datetime(2023, 10, 16, 16))
    shift_evening_mon = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 16, 16), datetime(2023, 10, 16, 22))
    shift_closing_mon = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 16, 19, 30), datetime(2023, 10, 17, 2))

    shift_morning_tue = Shift(ShiftTypesEnum.MORNING, datetime(2023, 10, 17, 10), datetime(2023, 10, 17, 16))
    shift_evening_tue = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 17, 16), datetime(2023, 10, 17, 22))
    shift_closing_tue = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 17, 19, 30), datetime(2023, 10, 18, 2))

    shift_morning_wed = Shift(ShiftTypesEnum.MORNING, datetime(2023, 10, 18, 10), datetime(2023, 10, 18, 16))
    shift_evening_wed = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 18, 16), datetime(2023, 10, 18, 22))
    shift_closing_wed = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 18, 19, 30), datetime(2023, 10, 19, 2))

    shift_morning_thu = Shift(ShiftTypesEnum.MORNING, datetime(2023, 10, 19, 10), datetime(2023, 10, 19, 16))
    shift_evening_thu = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 19, 16), datetime(2023, 10, 19, 22))
    shift_backup_thu = Shift(ShiftTypesEnum.THURSDAY_BACKUP, datetime(2023, 10, 19, 19, 30), datetime(2023, 10, 20, 0, 0, 0))
    shift_closing_thu = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 19, 21, 30), datetime(2023, 10, 20, 2))

    shift_morning_fri = Shift(ShiftTypesEnum.WEEKEND_MORNING, datetime(2023, 10, 20, 9, 15), datetime(2023, 10, 20, 18))
    shift_backup_fri = Shift(ShiftTypesEnum.WEEKEND_MORNING_BACKUP, datetime(2023, 10, 20, 12), datetime(2023, 10, 20, 18))
    shift_evening_fri = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 20, 18), datetime(2023, 10, 20, 22))
    shift_closing_fri = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 20, 21, 30), datetime(2023, 10, 21, 2))

    shift_morning_sat = Shift(ShiftTypesEnum.WEEKEND_MORNING, datetime(2023, 10, 21, 10), datetime(2023, 10, 21, 16))
    shift_backup_sat = Shift(ShiftTypesEnum.WEEKEND_MORNING_BACKUP, datetime(2023, 10, 21, 12), datetime(2023, 10, 21, 18))
    shift_evening_sat = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 21, 18), datetime(2023, 10, 21, 22))
    shift_closing_sat = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 21, 19, 30), datetime(2023, 10, 22, 2))

    employee1 = Employee("noa", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    employee2 = Employee("beny", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 2)
    employee3 = Employee("dan", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 3)
    employee4 = Employee("yahalom", EmployeePriorityEnum.MEDIUM, EmployeeStatusEnum.senior_employee, 4)

    cons = Constraints([employee1, employee2, employee3, employee4], [shift_morning_sun, shift_evening_sun, shift_closing_sun,
                                                           shift_morning_mon, shift_evening_mon, shift_closing_mon,
                                                           shift_morning_tue, shift_evening_tue, shift_closing_tue,
                                                           shift_morning_wed, shift_evening_wed, shift_closing_wed,
                                                           shift_morning_thu, shift_evening_thu, shift_backup_thu, shift_closing_thu,
                                                           shift_morning_fri, shift_backup_fri, shift_evening_fri, shift_closing_fri,
                                                           shift_morning_sat, shift_backup_sat, shift_evening_sat, shift_closing_sat])
    cons.add_only_one_employee_in_each_shift_constraint()
    cons.add_at_most_one_shift_that_starts_in_the_same_day_constraint()
    cons.add_constraint_to_prevent_new_employees_working_together(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING)
    cons.add_no_morning_shift_after_closing_shift_constraint()
    cons.objective_function()


if __name__ == "__main__":
    test()
    print("Hello World!")
