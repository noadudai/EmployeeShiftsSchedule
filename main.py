import datetime
from uuid import uuid4

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_at_most_one_shift_per_employee_in_the_same_day_constraint, add_limit_employees_working_days_constraint
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.frozen_shift_combinations_key import ShiftCombinationsKey
from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum


def create_schedule(employees: list[Employee], shifts: list[Shift]) -> list[tuple[Employee, Shift]]:
    schedule = []
    max_working_days = 2

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_at_most_one_shift_per_employee_in_the_same_day_constraint(shifts, employees, constraint_model, all_shifts)
    add_limit_employees_working_days_constraint(shifts, employees, constraint_model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    if status == cp_model.OPTIMAL:
        for employee in employees:
            for shift in shifts:

                if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                    schedule.append((employee, shift))

    if schedule:
        return schedule
    else:
        raise Exception("Empty schedule. No Optimal solution found.")


if __name__ == "__main__":
    jane = Employee("jane", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    doe = Employee("doe", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())
    dani = Employee("dani", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, employee_id=uuid4())

    employees = [jane, doe, dani]

    test_shift1 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 11, 9, 30), end_time=datetime.datetime(2023, 12, 11, 16, 0))
    test_shift2 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2023, 12, 11, 16, 0), end_time=datetime.datetime(2023, 12, 11, 22, 0))
    test_shift3 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 12, 16, 0), end_time=datetime.datetime(2023, 12, 12, 22, 0))
    test_shift4 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2023, 12, 12, 16, 0), end_time=datetime.datetime(2023, 12, 13, 22, 0))
    test_shift5 = Shift(shift_id=uuid4(), shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2023, 12, 13, 16, 0), end_time=datetime.datetime(2023, 12, 13, 22, 0))

    shifts = [test_shift1, test_shift2, test_shift3, test_shift4, test_shift5]

    try:
        schedule = create_schedule(employees, shifts)
        for employee, shift in schedule:
            print(f"{employee.name} is working {shift.shift_type.value} shift, that starts at {shift.start_time} and ends at {shift.end_time}")

    except Exception as e:
        print(e)
