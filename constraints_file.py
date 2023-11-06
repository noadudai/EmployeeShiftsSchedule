from itertools import pairwise
from datetime import timedelta
from typing import List
from ortools.sat.python import cp_model

from models.employees.employee import Employee
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shifts_enum import ShiftTypesEnum
from models.workers_schedule import WorkersWeekSchedule


# Returns a list containing all the "new employees" of each shift
def generate_new_employees_on_shift(employees, shifts, shift_combinations, shift_type: ShiftTypesEnum, day) -> list:
    employees_on_shift = []

    for employee in employees:
        for shift in shifts:

            start_date = shift.get_str_start_date_from_shift()
            end_date = shift.get_str_end_date_from_shift()

            if start_date == day and employee.status == EmployeeStatusEnum.new_employee and shift.type == shift_type:
                employees_on_shift.append(
                    shift_combinations[(employee.id, start_date, end_date, shift_type.value)])

    return employees_on_shift


# Returns a dictionary that contains all the combinations of shifts and employees as: the employee id, start date
#       (as a datetime object) of the shift, end date ( also as a datetime object) of the shift, and the shift's type,
#       as a key, and the value will be a boolean that will represent true or false based of if the employee is
#       working that shift or not.
def generate_shift_employee_combinations(employees: List[Employee], shifts: list[Shift], constraint_model) -> dict:
    combinations = {}
    for employee in employees:
        employee_id = employee.id

        for shift in shifts:
            start_date = shift.get_str_start_date_from_shift()
            end_date = shift.get_str_end_date_from_shift()
            shift_type = shift.type.value

            combinations[(employee_id, start_date, end_date, shift_type)] = constraint_model.NewBoolVar(
                    f"employee{employee_id}_start_date{start_date}_end_date{end_date}_shift{shift_type}")

    return combinations


# A constraint that ensures that there will be only one employee in each shift per day
def add_one_employee_per_shift_constraint(shifts: list[Shift], employees: List[Employee], constraint_model, shift_combinations) -> None:
    for shift in shifts:
        end_date = shift.get_str_end_date_from_shift()
        start_date = shift.get_str_start_date_from_shift()

        constraint_model.AddExactlyOne(shift_combinations[(employee.id, start_date, end_date, shift.type.value)] for employee in employees)


# A constraint that ensures that each employee works at most one shift per day
def add_at_most_one_shift_in_the_same_day_constraint(shifts: list[Shift], employees: List[Employee], constraint_model, shift_combinations) -> None:
    days_in_the_given_shift_list = list(set(shift.get_start_date_of_shift() for shift in shifts))

    for day in days_in_the_given_shift_list:
        for employee in employees:
            # a list of all the shifts that the employee is working on that day
            works_shifts_on_day = []

            for shift in shifts:
                start_date = shift.get_str_start_date_from_shift()
                end_date = shift.get_str_end_date_from_shift()

                if start_date == day:
                    works_shifts_on_day.append(shift_combinations[(employee.id, start_date, end_date, shift.type.value)])

            constraint_model.AddAtMostOne(works_shifts_on_day)


# A constraint that ensures that on each day, there is no new employee in the given first shift and a new employee
# in the given second shift
def add_prevent_new_employees_working_together_constraint(first_shift: ShiftTypesEnum, second_shift: ShiftTypesEnum, shifts: list[Shift], employees: List[Employee], constraint_model, shift_combinations) -> None:
    days_in_the_given_shift_list = list(set(shift.get_str_start_date_from_shift() for shift in shifts))

    for day in days_in_the_given_shift_list:
        # collecting all the new employees that are working on this day is specific shifts.
        new_employees_on_first_shift = generate_new_employees_on_shift(employees, shifts, shift_combinations, first_shift, day)
        new_employees_on_second_shift = generate_new_employees_on_shift(employees, shifts, shift_combinations, second_shift,  day)

        # The solver will try different combinations of values for these booleans while exploring the solution space
        # to find a valid assignment of employees to shifts that satisfies all constraints
        condition_shift1 = constraint_model.NewBoolVar(f"condition_shift1_{day}")
        condition_shift2 = constraint_model.NewBoolVar(f"condition_shift2_{day}")

        # if there's at least one new employee on shift1, condition_shift1 must be true,
        # and if there's no new employee on shift1, condition_shift1 must be false.
        constraint_model.Add(sum(new_employees_on_first_shift) >= 1).OnlyEnforceIf(condition_shift1)
        constraint_model.Add(sum(new_employees_on_first_shift) == 0).OnlyEnforceIf(condition_shift1.Not())

        constraint_model.Add(sum(new_employees_on_second_shift) >= 1).OnlyEnforceIf(condition_shift2)
        constraint_model.Add(sum(new_employees_on_second_shift) == 0).OnlyEnforceIf(condition_shift2.Not())

        # Implication: if there's a new employee on shift1, there cannot be a new employee on shift2
        constraint_model.AddBoolOr([condition_shift1.Not(), condition_shift2.Not()])


# A constraint that ensures that each employee does not work more than 6 days in a week
def add_max_working_days_a_week_constraint(shifts: list[Shift], employees: List[Employee], constraint_model, shift_combinations, max_working_days) -> None:
    # The max working days for an employee in a week is 6 by law.

    # Count the shifts an employee is assigned to.
    total_shifts_worked = {}

    for employee in employees:
        total_shifts_worked[employee.id] = sum(shift_combinations[(
            employee.id, shift.get_str_start_date_from_shift(), shift.get_str_end_date_from_shift(), shift.type.value)
        ] for shift in shifts)

    # ensure that the total shifts worked by each employee is not more than 6.
    for employee in employees:
        constraint_model.Add(total_shifts_worked[employee.id] <= max_working_days)


# A constraint that ensures that only an employee who asked for a day-off in advance will get that day off.
# And if not, the solver will assign an employee based on needs.
def add_employee_day_off_request_constraint(self) -> None:
    pass


# A constraint that ensures that, an employee working a closing shift will not have a morning shift the next day.
def add_no_morning_shift_after_closing_shift_constraint(shifts: list[Shift], employees: List[Employee], constraint_model, shift_combinations) -> None:
    for employee in employees:
        worked_closing_shift_yesterday = constraint_model.NewBoolVar(f"{employee.id}_worked_closing_shift_yesterday_day")

        for shift_pair in pairwise(shifts):
            first_shift, second_shift = shift_pair

            if first_shift.type == ShiftTypesEnum.CLOSING:
                start_closing_shift = first_shift.get_str_start_date_from_shift()
                end_closing_shift = first_shift.get_str_end_date_from_shift()

                start_morning_shift = second_shift.get_str_start_date_from_shift()
                end_morning_shift = second_shift.get_str_end_date_from_shift()

                constraint_model.Add(worked_closing_shift_yesterday == shift_combinations.get((employee.id, start_closing_shift, end_closing_shift, first_shift.type.value), 0))

                constraint_model.Add(shift_combinations[(employee.id, start_morning_shift, end_morning_shift, second_shift.type.value)] == 0).OnlyEnforceIf(
                    (second_shift.get_start_date_of_shift() - first_shift.get_end_date_of_shift()) >= timedelta(hours=24)
                )


def create_optimal_schedule(shifts: list[Shift], employees: List[Employee], constraint_model, shift_combinations) -> WorkersWeekSchedule:
    # need maximize on priority and preferences of the employees
    solver = cp_model.CpSolver()
    status = solver.Solve(constraint_model)
    if status == cp_model.OPTIMAL:
        schedule_shifts = []
        for shift in shifts:

            working_shift = Shift(shift.type, shift.start_date_and_time_of_shift, shift.end_date_and_time_of_shift)

            for employee in employees:
                if solver.Value(shift_combinations[(
                        employee.id, working_shift.get_str_start_date_from_shift(),
                        working_shift.get_str_end_date_from_shift(),
                        working_shift.type.value)]):

                    schedule_shifts.append([working_shift, employee])
                    break
        return WorkersWeekSchedule(schedule_shifts)
    else:
        print("No optimal solution found !")
