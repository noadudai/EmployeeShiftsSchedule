import datetime
from uuid import uuid4

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.frozen_shift_combinations_key import FrozenShiftCombinationsKey
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


def create_schedule(employees: list[Employee], shifts: list[Shift]) -> list[tuple[Employee, Shift]]:
    schedule = []

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    if status == cp_model.OPTIMAL:
        for employee in employees:
            for shift in shifts:

                if solver.Value(all_shifts[FrozenShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                    schedule.append((employee, shift))

    if schedule:
        return schedule
    else:
        raise Exception("Empty schedule. No Optimal solution found.")


if __name__ == "__main__":
    jane = Employee("jane", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    doe = Employee("doe", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())

    employees = [jane, doe]

    test_shift = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))

    try:
        schedule = create_schedule(employees, [test_shift])
        for employee, shift in schedule:
            print(f"{employee.name} is working {shift.shift_type.value} shift, that starts at {shift.start_time} and ends at {shift.end_time}")

    except Exception as e:
        print(e)
