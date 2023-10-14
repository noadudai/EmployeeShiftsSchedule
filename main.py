from models.employees.employee import Employee, EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.days.day import Day, DaysEnum
from models.shifts.shifts_enum import ShiftsEnum


def test():
    shift = Shift(ShiftsEnum.MORNING)
    employee = Employee("noa", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, [])

    assert (shift.employee == None)

    shift.set_employee(employee)

    assert (shift.employee.name == "noa")

    day = Day(DaysEnum.SUNDAY, [shift])

    assert (day.shifts[0].type == ShiftsEnum.MORNING)


if __name__ == "__main__":
    test()
    print("Hello World!")
