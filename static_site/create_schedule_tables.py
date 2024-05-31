import os
import uuid

from ortools.sat.python import cp_model
import pandas as pd

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint
from models.employees.employee import Employee
from models.employees.employees_file import all_employees
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_file import all_shifts_in_the_week
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.solution.one_schedule_solution import Solution
from models.solution.schedule_solutions import ScheduleSolutions


def create_schedules(employees: list[Employee], shifts: list[Shift]) -> ScheduleSolutions:
    max_working_days = 6

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    # add_limit_employees_working_days_constraint(shifts, employees, constraint_model, all_shifts, max_working_days)
    # add_minimum_time_between_a_morning_shift_and_the_shift_before_constraint(shifts, employees, constraint_model, all_shifts, datetime.timedelta(hours=9), early_morning_start_time=datetime.time(6), afternoon_start_time=datetime.time(12, 30))
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees,
                                                                                                      constraint_model,
                                                                                                      all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()
    previous_solution = set()
    count = 0

    print("Creating schedules")
    solutions = []
    while count <= 2:

        status = solver.Solve(constraint_model)

        if status == cp_model.OPTIMAL:
            solution_identifier = frozenset(
                ShiftCombinationsKey(employee.employee_id, shift.shift_id) for employee in employees for shift in shifts
                if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)])
                )

            if solution_identifier not in previous_solution:
                previous_solution.add(solution_identifier)

                number_of_closing_shifts_for_employees: dict[uuid.uuid4, int] = {}
                number_of_mornings_for_employees: dict[uuid.uuid4, int] = {}
                number_of_shift_for_employees: dict[uuid.uuid4, int] = {}

                for employee in employees:
                    number_of_closing_shifts_for_employees[employee.employee_id] = 0
                    number_of_mornings_for_employees[employee.employee_id] = 0
                    number_of_shift_for_employees[employee.employee_id] = 0

                schedule: dict[Shift, Employee] = {}

                for employee in employees:
                    for shift in shifts:
                        if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                            schedule[shift] = employee

                            number_of_shift_for_employees[employee.employee_id] += 1
                            if shift.shift_type == ShiftTypesEnum.CLOSING:
                                number_of_closing_shifts_for_employees[employee.employee_id] += 1
                            if shift.shift_type in [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP,
                                                    ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP]:
                                number_of_mornings_for_employees[employee.employee_id] += 1
                solution = Solution(number_of_closing_shifts_for_employees, number_of_mornings_for_employees,
                                    number_of_shift_for_employees, schedule)
                solutions.append(solution)
                count += 1

        else:
            print("No optimal solution found !")
            break

    print("done")
    schedule_solution = ScheduleSolutions(solutions)

    return schedule_solution


def data_frame_schedule_to_html_table(schedule: dict[Shift, Employee], shifts: list[Shift]) -> str:
    sorted_schedule = sorted(schedule.items(), key=lambda shift_emp_pair: shift_emp_pair[0].start_time)

    dates = [shift.start_time.date() for shift in shifts]
    unique_dates = sorted(set(str(date) for date in dates))

    shift_types = [ShiftTypesEnum.MORNING.value, ShiftTypesEnum.MORNING_BACKUP.value,
                   ShiftTypesEnum.WEEKEND_MORNING_BACKUP.value, ShiftTypesEnum.EVENING.value,
                   ShiftTypesEnum.THURSDAY_BACKUP.value,
                   ShiftTypesEnum.WEEKEND_EVENING_BACKUP.value, ShiftTypesEnum.CLOSING.value]

    data_frame = pd.DataFrame(index=shift_types, columns=unique_dates)

    for shift, emp in sorted_schedule:

        frame = ShiftTypesEnum.MORNING.value if shift.shift_type == ShiftTypesEnum.WEEKEND_MORNING else shift.shift_type.value

        shift_emp_times_str = f"{emp.name}<br> {str(shift.start_time.time())} - {str(shift.end_time.time())}"
        data_frame.at[frame, str(shift.start_time.date())] = shift_emp_times_str

    data_frame.fillna("", inplace=True)
    html_table = data_frame.to_html(escape=False)

    return html_table


def replace_html_tables_content_with_new_schedule_tables(all_schedules_string, name_of_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, name_of_file)

    with open(file_path, 'r', encoding='utf-8') as html_file_reader:
        html_content = html_file_reader.read()

    start_index_of_table = html_content.find('<div>') + len('<div>')
    # find, finds the first index of what i am searching for
    end_index_of_table = html_content.find('</div>', start_index_of_table) - 1

    new_file_content = html_content[:start_index_of_table] + '\n' + all_schedules_string + '\n'+ html_content[end_index_of_table:]

    with open(file_path, 'w', encoding='utf-8') as html_new_file:
        html_new_file.writelines(new_file_content)


def schedule_testing():
    employees = all_employees
    shifts = all_shifts_in_the_week

    try:
        schedule = create_schedules(employees, shifts)
        all_schedules = ''
        for solution in range(len(schedule.solutions)):
            # starts from 0
            all_schedules += f'solution {solution + 1}\n' + data_frame_schedule_to_html_table(schedule.solutions[solution].schedule, shifts) + '<br><br>'
        replace_html_tables_content_with_new_schedule_tables(all_schedules, "visual_schedule.html")
    except Exception as e:
        print(e)
