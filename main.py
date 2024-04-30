import datetime
import uuid
from uuid import uuid4
from ortools.sat.python import cp_model


from constraints_file import *
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.employees.employees_file import all_employees
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shift import Shift
from models.shifts.shifts_file import all_shifts_in_the_week
from models.shifts.shifts_types_enum import ShiftTypesEnum
from test.var_array_solution_printer import VarArraySolutionPrinter


def create_schedule(employees: list[Employee], shifts: list[Shift]) ->  dict[int, list[tuple[Employee, Shift]]]:
    schedule = {}
    max_working_days = 6

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    # add_limit_employees_working_days_constraint(shifts, employees, constraint_model, all_shifts, max_working_days)
    # add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, constraint_model, all_shifts, datetime.timedelta(hours=9), early_morning_start_time=datetime.time(6), afternoon_start_time=datetime.time(12, 30))
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    previous_solution = set()
    count = 0
    while count <= 5:

        status = solver.Solve(constraint_model)

        if status == cp_model.OPTIMAL:
            solution_identifier = frozenset(ShiftCombinationsKey(employee.employee_id, shift.shift_id) for employee in employees for shift in shifts
                if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)])
            )

            solution = []
            if solution_identifier not in previous_solution:
                previous_solution.add(solution_identifier)

            for employee in employees:
                for shift in shifts:
                    if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                        solution.append((employee, shift))

            solution.sort(key=lambda shift_employee_pair: shift_employee_pair[1].start_time)
            schedule[count] = solution
            count += 1

        else:
            print("No optimal solution found !")
            break

    print("done")
    return schedule


if __name__ == "__main__":

    employees = all_employees
    shifts = all_shifts_in_the_week

    try:
        schedule = create_schedule(employees, shifts)
        for count, employee_shift in schedule.items():
            print(f"solution {count}")
            for employee, shift in employee_shift:
                print(f"{employee.name} is working {shift.shift_type.value} shift, that starts at {shift.start_time} and ends at {shift.end_time}")
            print()
    except Exception as e:
        print(e)
