import datetime
import uuid

from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_limit_employees_working_days_constraint, add_minimum_time_between_closing_shift_and_next_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint
from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_preferences.day_preference import DayOffPreference
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.solution.schedule_solution import ScheduleSolution

pinchass_preferences = Preferences(days_cannot_work=
                                   [DayOffPreference(datetime.date(2024, 3, 24))],
                                   days_prefer_not_to_work=
                                   [DayOffPreference(datetime.date(2024, 3, 30))],
                                   shifts_prefer_to_work_in_days=
                                   [ShiftsPreference(datetime.date(2024, 3, 26), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
                                    ShiftsPreference(datetime.date(2024, 4, 29), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

kuzus_preferences = Preferences(days_cannot_work=
                                [DayOffPreference(datetime.date(2024, 3, 24))],
                                shifts_prefer_to_work_in_days=
                                [ShiftsPreference(datetime.date(2024, 3, 25), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                 ShiftsPreference(datetime.date(2024, 3, 30), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

itays_preferences = Preferences(days_cannot_work=
                                [DayOffPreference(datetime.date(2024, 3, 24))],
                                days_prefer_not_to_work=
                                [DayOffPreference(datetime.date(2024, 3, 29))],
                                shifts_prefer_to_work_in_days=
                                [ShiftsPreference(datetime.date(2024, 3, 25), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                 ShiftsPreference(datetime.date(2024, 3, 26), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
                                 ShiftsPreference(datetime.date(2024, 3, 27), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING])])

yossis_preferences = Preferences(shifts_prefer_to_work_in_days=
                                 [ShiftsPreference(datetime.date(2024, 3, 28), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                  ShiftsPreference(datetime.date(2024, 3, 29), [ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING]),
                                  ShiftsPreference(datetime.date(2024, 3, 30), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

chapos_preferences = Preferences(shifts_prefer_to_work_in_days=
                                 [ShiftsPreference(datetime.date(2024, 3, 28), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                  ShiftsPreference(datetime.date(2024, 3, 30), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])
idos_preferences = Preferences(days_cannot_work=
                               [DayOffPreference(datetime.date(2024, 3, 26)),
                                DayOffPreference(datetime.date(2024, 3, 27)),
                                DayOffPreference(datetime.date(2024, 3, 28))],
                               shifts_prefer_to_work_in_days=
                               [ShiftsPreference(datetime.date(2024, 3, 25), [ShiftTypesEnum.EVENING]),
                                ShiftsPreference(datetime.date(2024, 3, 29), [ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING])])

noa = Employee(name="Noa", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="noa", shift_types_trained_to_do=[ShiftTypesEnum.EVENING, ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.WEEKEND_MORNING])
pinchas = Employee(name="Pinchas", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="pinchas", preferences=pinchass_preferences, shift_types_trained_to_do=[ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING])
kuzu = Employee(name="Kuzu", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="kuzu", preferences=kuzus_preferences, shift_types_trained_to_do=[ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING])
itay = Employee(name="itay", priority=EmployeePriorityEnum.LOW, employee_status=EmployeeStatusEnum.junior_employee, employee_id="itay", preferences=itays_preferences, shift_types_trained_to_do=[ShiftTypesEnum.CLOSING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])
yossi = Employee(name="yossi", priority=EmployeePriorityEnum.LOW, employee_status=EmployeeStatusEnum.mid_level_employee, employee_id="yossi", preferences=yossis_preferences, shift_types_trained_to_do=[ShiftTypesEnum.CLOSING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])
chapo = Employee(name="chapo", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="chapo", preferences=chapos_preferences, shift_types_trained_to_do=[ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING])
ido = Employee(name="ido", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="ido", preferences=idos_preferences, shift_types_trained_to_do=[ShiftTypesEnum.EVENING, ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])

shifts_this_week = [Shift(shift_id="2024, 3, 24, morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 3, 24, 9, 30), end_time=datetime.datetime(2024, 3, 24, 17, 0)),
                    Shift(shift_id="2024, 3, 24, morning backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 24, 3, 0), end_time=datetime.datetime(2024, 3, 24, 17, 0)),
                    Shift(shift_id="2024, 3, 24, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 24, 16, 0), end_time=datetime.datetime(2024, 3, 25, 0)),
                    Shift(shift_id="2024, 3, 24, closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 24, 19, 30), end_time=datetime.datetime(2024, 3, 25, 2, 0)),
                    Shift(shift_id="2024, 3, 25, morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 3, 25, 9, 30), end_time=datetime.datetime(2024, 3, 25, 17, 0)),
                    Shift(shift_id="2024, 3, 25, morning backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 25, 3, 0), end_time=datetime.datetime(2024, 3, 25, 17, 0)),
                    Shift(shift_id="2024, 3, 25, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 25, 16, 0), end_time=datetime.datetime(2024, 3, 26, 0)),
                    Shift(shift_id="2024, 3, 25, closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 25, 19, 30), end_time=datetime.datetime(2024, 3, 26, 2, 0)),
                    Shift(shift_id="2024, 3, 26, morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 3, 26, 9, 30), end_time=datetime.datetime(2024, 3, 26, 17, 0)),
                    Shift(shift_id="2024, 3, 26, morning backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 26, 3, 0), end_time=datetime.datetime(2024, 3, 26, 17, 0)),
                    Shift(shift_id="2024, 3, 26, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 26, 16, 0), end_time=datetime.datetime(2024, 3, 27, 0)),
                    Shift(shift_id="2024, 3, 26, closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 26, 19, 30), end_time=datetime.datetime(2024, 3, 27, 2, 0)),
                    Shift(shift_id="2024, 3, 27, morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 3, 27, 9, 30), end_time=datetime.datetime(2024, 3, 27, 17, 0)),
                    Shift(shift_id="2024, 3, 27, morning backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 27, 3, 0), end_time=datetime.datetime(2024, 3, 27, 17, 0)),
                    Shift(shift_id="2024, 3, 27, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 27, 16, 0), end_time=datetime.datetime(2024, 3, 28, 0)),
                    Shift(shift_id="2024, 3, 27, closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 27, 19, 30), end_time=datetime.datetime(2024, 3, 28, 2, 0)),
                    Shift(shift_id="2024, 3, 28, morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 3, 28, 9, 30), end_time=datetime.datetime(2024, 3, 28, 17, 0)),
                    Shift(shift_id="2024, 3, 28, morning backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 28, 3, 0), end_time=datetime.datetime(2024, 3, 28, 17, 0)),
                    Shift(shift_id="2024, 3, 28, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 28, 15, 0), end_time=datetime.datetime(2024, 3, 29, 0, 0)),
                    Shift(shift_id="2024, 3, 28, thursday backup", shift_type=ShiftTypesEnum.THURSDAY_BACKUP, start_time=datetime.datetime(2024, 3, 28, 19, 30), end_time=datetime.datetime(2024, 3, 29, 2, 0)),
                    Shift(shift_id="2024, 3, 28, closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 28, 21, 0), end_time=datetime.datetime(2024, 3, 29, 2, 0)),
                    Shift(shift_id="2024, 3, 29, weekend morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 3, 29, 7, 30), end_time=datetime.datetime(2024, 3, 29, 14, 30)),
                    Shift(shift_id="2024, 3, 29, weekend morning backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 29, 8, 0), end_time=datetime.datetime(2024, 3, 29, 17, 0)),
                    Shift(shift_id="2024, 3, 29, weekend morning backup2", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 29, 11, 30), end_time=datetime.datetime(2024, 3, 29, 19, 0)),
                    Shift(shift_id="2024, 3, 29, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 29, 16, 30), end_time=datetime.datetime(2024, 3, 30, 0, 0)),
                    Shift(shift_id="2024, 3, 29, weekend evening backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 3, 29, 21, 30), end_time=datetime.datetime(2024, 3, 30, 2, 0)),
                    Shift(shift_id="2024, 3, 29, closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 29, 22, 0), end_time=datetime.datetime(2024, 3, 30, 2, 0)),
                    Shift(shift_id="2024, 3, 30, weekend morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 3, 30, 7, 30), end_time=datetime.datetime(2024, 3, 30, 18, 0)),
                    Shift(shift_id="2024, 3, 30, weekend morning backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 30, 7, 30), end_time=datetime.datetime(2024, 3, 30, 18, 0)),
                    Shift(shift_id="2024, 3, 30, weekend morning backup2", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 3, 30, 12, 0), end_time=datetime.datetime(2024, 3, 30, 18, 0)),
                    Shift(shift_id="2024, 3, 30, evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 3, 30, 17, 0), end_time=datetime.datetime(2024, 3, 31, 0, 0)),
                    Shift(shift_id="2024, 3, 30, weekend evening backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 3, 30, 17, 0), end_time=datetime.datetime(2024, 3, 31, 2, 0)),
                    Shift(shift_id="2024, 3, 30 , closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 3, 30, 19, 30), end_time=datetime.datetime(2024, 3, 31, 2, 0)),
                    ]


def create_schedule(employees: list[Employee], shifts: list[Shift]) ->  list[ScheduleSolution]:
    schedule = []

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_limit_employees_working_days_constraint(shifts, employees, constraint_model, all_shifts, 6)
    add_minimum_time_between_closing_shift_and_next_shift_constraint(shifts, employees, constraint_model, all_shifts, datetime.timedelta(hours=9))
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()

    solution = []
    previous_solution = set()
    count = 0
    while count <= 4:
        number_of_shifts_this_week = {}
        number_of_closings = {}
        number_of_mornings = {}
        for employee in employees:
            number_of_shifts_this_week[employee.employee_id] = 0
            number_of_closings[employee.employee_id] = 0
            number_of_mornings[employee.employee_id] = 0

        status = solver.Solve(constraint_model)

        if status == cp_model.OPTIMAL:
            solution_identifier = frozenset(
                (employee.employee_id, shift.shift_id) for shift in shifts for employee in
                employees
                if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)])
            )

            if solution_identifier not in previous_solution:
                previous_solution.add(solution_identifier)

                shift_employee = {}
                for shift in shifts:

                    for employee in employees:
                        if solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                            number_of_shifts_this_week[employee.employee_id] += 1
                            if shift.shift_type == ShiftTypesEnum.CLOSING:
                                number_of_closings[employee.employee_id] += 1
                            if shift.shift_type == ShiftTypesEnum.MORNING or shift.shift_type == ShiftTypesEnum.MORNING_BACKUP or shift.shift_type == ShiftTypesEnum.WEEKEND_MORNING or shift.shift_type == ShiftTypesEnum.WEEKEND_MORNING_BACKUP:
                                number_of_mornings[employee.employee_id] += 1

                            shift_employee[shift.shift_id] = employee.employee_id
                            break

                schedule_solution = ScheduleSolution(shift_employee, number_of_shifts_this_week, number_of_closings, number_of_mornings)
                solution.append(schedule_solution)
                count += 1
        else:
            print("No optimal solution found !")
    return solution


if __name__ == "__main__":
    employees = [noa, pinchas, kuzu,itay, yossi, chapo, ido]

    schedules = create_schedule(employees, shifts_this_week)
    print("schedules created")
