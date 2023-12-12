import datetime

from ortools.sat.python import cp_model

from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.frozen_shift_combinations_key import FrozenShiftCombinationKey
from models.shifts.shift import Shift
from models.shifts.shift_type import ShiftType
from models.shifts.shifts_types_enum import ShiftTypesEnum
from smaller_constraints import add_at_most_one_shift_for_employee_in_a_day_constrain, generate_shift_employee_combinations, \
    add_at_least_one_employee_per_shift_constraint


def create_schedule(employees: list[Employee], shifts_for_schedule: list[Shift]) -> list[tuple[Shift, Employee]]:
    schedule = []

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations(employees, shifts_for_schedule, constraint_model)

    employees_on_shift = [shift_combinations[FrozenShiftCombinationKey(employee.id, test_shift.start_date_of_shift, test_shift.end_date_of_shift, test_shift.shift_type.name_of_shift)] for employee in employees]
    add_at_least_one_employee_per_shift_constraint(constraint_model, employees_on_shift)

    days_in_the_given_shift_list = list(set(shift.start_date_of_shift for shift in shifts_for_schedule))
    for day in days_in_the_given_shift_list:
        for shift in shifts_for_schedule:
            start_date = shift.start_date_of_shift

            if start_date == day:
                works_shifts_on_day = [shift_combinations[FrozenShiftCombinationKey(employee.id, shift.start_date_of_shift, shift.end_date_of_shift, shift.shift_type.name_of_shift)] for employee in employees]
                add_at_most_one_shift_for_employee_in_a_day_constrain(constraint_model, works_shifts_on_day)

    constraint_model = cp_model.CpModel()
    shift_combinations = generate_shift_employee_combinations(employees, shifts_for_schedule, constraint_model)

    for shift in shifts_for_schedule:
        employees_on_shift = [shift_combinations[FrozenShiftCombinationKey(employee.id, shift.start_date_of_shift, shift.end_date_of_shift, shift.shift_type.name_of_shift)] for employee in employees]

        add_at_least_one_employee_per_shift_constraint(constraint_model, employees_on_shift)

    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)

    if status == cp_model.OPTIMAL:
        for employee in employees:
            for shift in shifts_for_schedule:
                start_shift = test_shift.start_date_of_shift
                end_shift = test_shift.end_date_of_shift
                shift_type = test_shift.shift_type.name_of_shift

                if solver.Value(shift_combinations[FrozenShiftCombinationKey(employee.id, start_shift, end_shift, shift_type)]):
                    schedule.append((shift, employee))

    return schedule


if __name__ == "__main__":
    jane = Employee("jane", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    doe = Employee("doe", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    employees = [jane, doe]

    start_time_of_shift = datetime.time(9, 30)
    start_date_of_shift = datetime.date(2023, 11, 12)
    end_time_of_shift = datetime.time(16, 0)
    end_date_of_shift = datetime.date(2023, 11, 12)

    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, start_time_of_shift, end_time_of_shift), start_date_of_shift,
                       end_date_of_shift)

    schedule = create_schedule(employees, [test_shift])

    for shift_employee_pair in schedule:
        shift, employee = shift_employee_pair
        print(f"shift {shift.shift_type.name_of_shift.value} starts at {shift.start_date_of_shift} {shift.shift_type.start_time}. the employee working the shift is {employee}")
