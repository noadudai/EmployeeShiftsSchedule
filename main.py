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
    shift_morning = Shift(ShiftTypesEnum.MORNING, datetime(2023, 10, 16, 10), datetime(2023, 10, 16, 16))
    shift_evening = Shift(ShiftTypesEnum.EVENING, datetime(2023, 10, 16, 16), datetime(2023, 10, 16, 22))
    shift_closing = Shift(ShiftTypesEnum.CLOSING, datetime(2023, 10, 16, 19, 30), datetime(2023, 10, 17, 2))

    employee1 = Employee("noa", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    employee2 = Employee("beny", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)
    employee3 = Employee("chep", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 3)

    cons = Constraints([employee1, employee2, employee3], [shift_morning, shift_evening, shift_closing])
    cons.add_only_one_employee_in_each_shift_constraint()
    cons.add_at_most_one_shift_that_starts_in_the_same_day_constraint()
    cons.objective_function()


if __name__ == "__main__":
    test()
    print("Hello World!")
