from Models.Employee_model import EmployeeModel, PriorityEnum
from Models.Shifts_model import ShiftsModel
from Models.Day_model import DayModel, DaysEnum


def test():
    shift = ShiftsModel("morning")
    employee = EmployeeModel("noa", PriorityEnum.HIGHEST, False)

    assert (shift.employee == None)

    shift.set_employee(employee)

    assert (shift.employee.name == "noa")

    day = DayModel(DaysEnum.SUNDAY, [shift])

    assert (day.shifts[0].type == "morning")


if __name__ == "__main__":
    test()
    print("Hello World!")
