import datetime
from uuid import uuid4
from ortools.sat.python import cp_model

from constraints_file import *
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.employees.employees_file import this_weeks_employees
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shift import Shift
from models.shifts.shifts_file import week_21_to_27_to_april
from models.shifts.shifts_types_enum import ShiftTypesEnum


def create_schedule(employees: list[Employee], shifts: list[Shift]) -> list[tuple[Employee, Shift]]:
    schedule = []
    max_working_days = 6

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    # add_limit_employees_working_days_constraint(shifts, employees, constraint_model, all_shifts, max_working_days)
    afternoon_shift_keys = add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, constraint_model, all_shifts, datetime.timedelta(hours=9), early_morning_start_time=datetime.time(6), afternoon_start_time=datetime.time(12, 30))
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(list(afternoon_shift_keys.values()))
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(constraint_model, solution_printer)

    # solver = cp_model.CpSolver()
    # status = solver.Solve(constraint_model)

    if status == cp_model.OPTIMAL:
        for employee in employees:
            for shift in shifts:

                if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                    schedule.append((employee, shift))

    if schedule:
        shift_index = 1
        schedule.sort(key= lambda shift_employee_pair: shift_employee_pair[shift_index].start_time.date())
        return schedule
    else:
        raise Exception("Empty schedule. No Optimal solution found.")


if __name__ == "__main__":

    employees = this_weeks_employees
    shifts = week_21_to_27_to_april

    try:
        schedule = create_schedule(employees, shifts)
        for employee, shift in schedule:
            print(f"{employee.name} is working {shift.shift_type.value} shift, that starts at {shift.start_time} and ends at {shift.end_time}")

    except Exception as e:
        print(e)
