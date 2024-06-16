import datetime
import json
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
from models.solution.one_schedule_solution import Solution
from models.solution.schedule_solutions import ScheduleSolutions
from static_site.create_schedule_tables import data_frame_schedule_to_dictionary
from test.var_array_solution_printer import VarArraySolutionPrinter


def create_a_new_schedule(solver: cp_model.CpSolver, constraint_model: cp_model.CpModel, all_shifts: dict[ShiftCombinationsKey, IntVar], previous_solutions: set, employees: list[Employee], shifts: list[Shift]):
    status = solver.Solve(constraint_model)

    if status == cp_model.OPTIMAL:
        solution_identifier = frozenset(
            ShiftCombinationsKey(employee.employee_id, shift.shift_id) for employee in employees for shift in shifts
            if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)])
            )

        if solution_identifier not in previous_solutions:
            previous_solutions.add(solution_identifier)

            # creating dictionaries for data. how many shifts each employee got, how many morning shifts ect.
            num_closings_for_employees: dict[uuid.uuid4, int] = {}
            num_mornings_for_employees: dict[uuid.uuid4, int] = {}
            num_shift_for_employees: dict[uuid.uuid4, int] = {}

            for employee in employees:
                num_closings_for_employees[employee.employee_id] = 0
                num_mornings_for_employees[employee.employee_id] = 0
                num_shift_for_employees[employee.employee_id] = 0

            schedule: dict[uuid.uuid4(), uuid.uuid4()] = {}

            for employee in employees:
                for shift in shifts:
                    if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                        schedule[shift.shift_id] = employee.employee_id

                        num_shift_for_employees[employee.employee_id] += 1

                        if shift.shift_type == ShiftTypesEnum.CLOSING:
                            num_closings_for_employees[employee.employee_id] += 1

                        if shift.shift_type in [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP,
                                                ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP]:
                            num_mornings_for_employees[employee.employee_id] += 1

            solution = Solution(num_closings_for_employees, num_mornings_for_employees, num_shift_for_employees, schedule)

            return solution
    else:
        raise Exception("Schedule not created")


def create_schedule_options(employees: list[Employee], shifts: list[Shift], number_of_solutions: int) -> ScheduleSolutions:
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
    previous_solutions = set()
    count = 0

    print("Creating schedules")
    schedules = []
    while count <= (number_of_solutions - 1):

        schedule = create_a_new_schedule(solver, constraint_model, all_shifts, previous_solutions, employees, shifts)
        if schedule:
            schedules.append(schedule)
            count += 1

    schedules_options = ScheduleSolutions(schedules)

    print("done")
    return schedules_options


if __name__ == "__main__":
    employees = all_employees
    shifts = all_shifts_in_the_week
    number_of_solutions = 3

    try:
        schedules = create_schedule_options(employees, shifts, number_of_solutions)
        list_of_schedule_options = []
        for solution in schedules.solutions:
            list_of_schedule_options.append(data_frame_schedule_to_dictionary(solution.schedule, shifts, employees))

        with open("static_site/schedule_data.json", "w") as json_data_file:
            json.dump(list_of_schedule_options, json_data_file)

    except Exception as e:
        print(e)
