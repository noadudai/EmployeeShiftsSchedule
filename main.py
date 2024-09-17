import datetime
import json
import uuid
from collections import defaultdict
from uuid import uuid4
from ortools.sat.python import cp_model


from constraints_file import *
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.employees.pe_employees_file import all_employees
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shift import Shift
from models.shifts.pe_shifts_file import all_shifts_in_the_week
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.solution.one_schedule_solution import ScheduleSolution
from models.solution.schedule_solutions import ScheduleSolutions
from static_site.create_schedule_tables import schedule_to_json
from test.var_array_solution_printer import VarArraySolutionPrinter


def create_a_new_schedule(solver: cp_model.CpSolver, all_shifts: dict[ShiftCombinationsKey, IntVar], employees: list[Employee], shifts: list[Shift]):
    # creating dictionaries for data. how many shifts each employee got, how many morning shifts ect.
    num_closings_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)
    num_mornings_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)
    num_shift_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)

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

    solution = ScheduleSolution(num_closings_for_employees, num_mornings_for_employees, num_shift_for_employees, schedule)

    return solution


def create_schedule_options(employees: list[Employee], shifts: list[Shift], number_of_solutions: int) -> ScheduleSolutions:
    max_working_days = 6

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_limit_employees_working_days_constraint(shifts, employees, constraint_model, all_shifts, max_working_days)
    # add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, constraint_model, all_shifts, datetime.timedelta(hours=9), early_morning_start_time=datetime.time(6), afternoon_start_time=datetime.time(12, 30))
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    previous_solutions = set()

    print("Creating schedules")
    schedules = []
    while len(schedules) <= (number_of_solutions - 1):

        status = solver.Solve(constraint_model)

        if status == cp_model.OPTIMAL:
            possible_solution = frozenset(
                ShiftCombinationsKey(employee.employee_id, shift.shift_id) for employee in employees for shift in shifts
                if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)])
            )

            if possible_solution not in previous_solutions:
                previous_solutions.add(possible_solution)

                schedule = create_a_new_schedule(solver, all_shifts, employees, shifts)
                schedules.append(schedule)

    schedules_options = ScheduleSolutions(schedules)

    print("done")
    return schedules_options


def create_shift_dictionary_for_html(shifts: list[Shift]) -> dict[str, dict]:
    shift_dict: dict[str, dict] = {}

    for shift in shifts:
        shift_dict[str(shift.shift_id)] = {"shift_id": str(shift.shift_id), "shift_type": shift.shift_type.value, "shift_start_time": str(shift.start_time), "shift_end_time": str(shift.end_time)}
    return shift_dict


def create_employee_dictionary_for_html(employees: list[Employee]) -> dict[str, dict]:
    emp_dict: dict[str, dict] = {}

    for emp in employees:
        emp_dict[str(emp.employee_id)] = {"employee_name": emp.name, "employee_priority": emp.priority.value, "employee_status": emp.employee_status.value, "employee_id": emp.employee_id, "employee_position": emp.position.value}
    return emp_dict


if __name__ == "__main__":
    employees = all_employees
    shifts = all_shifts_in_the_week
    number_of_solutions = 2
    shift_dict = create_shift_dictionary_for_html(shifts)
    emp_dict = create_employee_dictionary_for_html(employees)

    try:
        print("getting schedules")
        schedules = create_schedule_options(employees, shifts, number_of_solutions)
        list_of_schedule_options = []
        additional_data: list[dict[str, defaultdict[uuid.UUID, int]]] = []

        for solution in schedules.solutions:
            list_of_schedule_options.append(schedule_to_json(solution.schedule, shifts, employees))
            metadata_for_schedule = {"number_of_shifts": solution.number_of_shift_for_each_emp, "number_morning_shifts": solution.number_of_mornings_for_each_emp, "number_closing_shifts":solution.number_of_closings_for_each_emp}
            additional_data.append(metadata_for_schedule)

        json_data = {"schedules": list_of_schedule_options, "employees": emp_dict, "shifts": shift_dict}
        with open("static_site/schedule_data.json", "w") as json_data_file:
            json.dump(json_data, json_data_file)

        # add data for how many shifts each employee gets,
        # how many closing shifts each employee gets and how many morning shifts each employee gets, to a json file.
        with open("static_site/employees_schedules_additional_data.json", "w") as additional_data_file:
            json.dump(additional_data, additional_data_file)

    except Exception as e:
        print(e)
