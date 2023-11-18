import datetime
from collections import Counter
from typing import List

from ortools.sat.python import cp_model
import pytest
from ortools.sat.python import cp_model


from constraints import *
from models.days_enum import DaysEnum
from models.employees.employee import Employee
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shift import Shift
from models.shifts.shift_type import ShiftType
from models.shifts.shifts_types_enum import ShiftTypesEnum


def test_add_one_employee_per_shift_constraint_broken_down():

    def add_one_employee_in_shift_constraint(employees_shift_assignment: List[bool], constraint_model) -> None:
        constraint_model.AddExactlyOne(employees_shift_assignment)

    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)
    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)),
                        datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift1], model)
    all_shifts_assignments = [shifts[(employee.id, test_shift1.get_str_start_date(), test_shift1.get_str_end_date(), test_shift1.shift_type.name_of_shift.value)] for employee in [test_employee, test_employee2]]

    add_one_employee_in_shift_constraint(all_shifts_assignments, model)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    assert (solver.Value(shifts[(
        test_employee2.id, test_shift1.get_str_start_date(),
        test_shift1.get_str_end_date(),
        test_shift1.shift_type.name_of_shift.value)]) == 0)

    assert (status == cp_model.OPTIMAL)


def test_add_one_employee_per_shift_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift1], model)

    add_one_employee_per_shift_constraint([test_shift1], [test_employee, test_employee2], model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    assert (solver.Value(shifts[(
                test_employee2.id, test_shift1.get_str_start_date(),
                test_shift1.get_str_end_date(),
                test_shift1.shift_type.name_of_shift.value)]) == 0)

    assert (status == cp_model.OPTIMAL)


def test_add_one_employee_per_shift_constraint_with_no_employees():
    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([], [test_shift1], model)

    add_one_employee_per_shift_constraint([test_shift1], [], model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Not an optimal solution because the constraint supposed to assign an employee to a shift,
    # and there is no employee to assign.
    assert (status != cp_model.OPTIMAL)


def test_add_at_most_one_shift_in_the_same_day_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)
    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(16, 0), datetime.time(22, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift1, test_shift2, test_shift3], model)

    add_at_most_one_shift_in_the_same_day_constraint([test_shift1, test_shift2, test_shift3], [test_employee, test_employee2], model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # there is a solution where employees are not assigned to shifts, which is considered an optimal solution.
    assert (status == cp_model.OPTIMAL)

    if status == cp_model.OPTIMAL:
        for shift in [test_shift1, test_shift2, test_shift3]:
            for employee in [test_employee, test_employee2]:
                # the employee does not work this shift
                assert (solver.Value(shifts[(employee.id, shift.get_str_start_date(),shift.get_str_end_date(), shift.shift_type.name_of_shift.value)]) == 0)


def test_add_at_most_one_shift_in_the_same_day_constraint_with_at_least_one_employee_in_a_shift():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)
    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(16, 0), datetime.time(22, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift1, test_shift2, test_shift3], model)

    # When adding the constraint "add_one_employee_per_shift_constraint", it also ensures that there is at least one
    # employee in each shift, causing "add_at_most_one_shift_in_the_same_day_constraint" to fail- because the solver
    # needs to assign at least one employee in each shift, and cannot assign an employee to more than 1 shift a day.
    add_one_employee_per_shift_constraint([test_shift1, test_shift2, test_shift3], [test_employee, test_employee2], model, shifts)
    add_at_most_one_shift_in_the_same_day_constraint([test_shift1, test_shift2, test_shift3], [test_employee, test_employee2], model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status != cp_model.OPTIMAL)


def test_add_prevent_new_employees_working_together_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 2)
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(16, 0), datetime.time(22, 0)),
                        datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)),
                        datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee, test_employee2],
                                                  [test_shift2, test_shift3], model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint([test_shift2, test_shift3], [test_employee, test_employee2],model, shifts)
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, [test_shift2, test_shift3], [test_employee, test_employee2], model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # 2 new employees, because of the "add_one_employee_per_shift_constraint" that ensures that there is at least one
    # employee in each shift, there is no optimal solution.
    assert (status != cp_model.OPTIMAL)


def test_add_no_morning_shift_after_closing_shift_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    test_shift2 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)),
                        datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))

    test_shift3 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)),
                        datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift2, test_shift3], model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint([test_shift2, test_shift3], [test_employee, test_employee2], model, shifts)
    add_no_morning_shift_after_closing_shift_constraint([test_shift2, test_shift3], [test_employee, test_employee2], model, shifts, timedelta(hours=12))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    # printing to see that the employee that worked in the closing shift is not the same employee of the morning shift
    for shift in [test_shift2, test_shift3]:
        for employee in [test_employee, test_employee2]:
            if solver.Value(shifts[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift.value)]):
                print(employee.id, shift.shift_type.name_of_shift.value)


def test_add_no_morning_shift_after_closing_shift_constraint_with_one_employee():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)

    test_shift2 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)),
                        datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)),
                        datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee], [test_shift2, test_shift3], model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint([test_shift2, test_shift3], [test_employee], model, shifts)
    add_no_morning_shift_after_closing_shift_constraint([test_shift2, test_shift3], [test_employee], model, shifts, datetime.timedelta(hours=12))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # failed because there is only one employee, and the time between the closing shift and the morning
    # shift the day after is less than 12 hours
    assert (status != cp_model.OPTIMAL)


def test_add_max_working_days_a_week_constraint_3_shifts_1_emp():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)

    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 14), datetime.date(2023, 11, 14))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 15), datetime.date(2023, 11, 15))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee], [test_shift1, test_shift2, test_shift3], model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint([test_shift1, test_shift2, test_shift3], [test_employee], model, shifts)
    add_max_working_days_a_week_constraint([test_shift1, test_shift2, test_shift3], [test_employee], model, shifts, 2)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Failed because there is only one employee, and there are 3 shifts. If there were 2 shifts, the solver would have
    # found an optimal solution where there is 1 employee in every shift, but combining the
    # "add_one_employee_per_shift_constraint" ensures that there is at least one employee in each shift, with the
    # "add_max_working_days_a_week_constraint" with 2 shifts max and a list of 3 shifts, creates an infeasible
    # solution with only 1 employee.
    assert (status != cp_model.OPTIMAL)


def test_add_max_working_days_a_week_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)

    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)),
                        datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)),
                        datetime.date(2023, 11, 14), datetime.date(2023, 11, 14))

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations([test_employee], [test_shift1, test_shift2], model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint([test_shift1, test_shift2], [test_employee], model, shifts)
    add_max_working_days_a_week_constraint([test_shift1, test_shift2], [test_employee], model, shifts,
                                           2)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)


# A function to generate the shifts from sunday to saturday
def generate_sun_to_sat_shifts_for_test(sunday: datetime.date, saturday: datetime.date, shifts):

    # these times are for testing.
    morning_shift = ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0))
    evening_shift = ShiftType(ShiftTypesEnum.EVENING, datetime.time(17, 0), datetime.time(22, 0))
    closing_shift = ShiftType(ShiftTypesEnum.CLOSING, datetime.time(19, 30), datetime.time(2, 0))
    thu_backup_shift = ShiftType(ShiftTypesEnum.THURSDAY_BACKUP, datetime.time(19, 30), datetime.time(22, 0))
    thu_closing_shift = ShiftType(ShiftTypesEnum.CLOSING, datetime.time(21, 0), datetime.time(2, 0))
    weekend_morning_shift = ShiftType(ShiftTypesEnum.WEEKEND_MORNING, datetime.time(9, 15), datetime.time(18, 0))
    weekend_backup_shift = ShiftType(ShiftTypesEnum.WEEKEND_MORNING_BACKUP, datetime.time(12, 0), datetime.time(18, 0))
    weekend_evening_shift = ShiftType(ShiftTypesEnum.EVENING, datetime.time(18, 0), datetime.time(22, 0))

    delta = datetime.timedelta(days=1)
    days = [sunday + datetime.timedelta(days=day) for day in range(0, (saturday - sunday).days + 1)]

    for day in days:
        if DaysEnum.THU.value < day.weekday() <= DaysEnum.SAT.value:
            shifts.append(Shift(weekend_morning_shift, day, day))
            shifts.append(Shift(weekend_backup_shift, day, day))
            shifts.append(Shift(weekend_evening_shift, day, day))
            shifts.append(Shift(closing_shift, day, day + delta))

        # sun to thu
        else:
            shifts.append(Shift(morning_shift, day, day))
            shifts.append(Shift(evening_shift, day, day))

            # if the day is thu
            if day.weekday() == DaysEnum.THU.value:
                shifts.append(Shift(thu_backup_shift, day, day))
                shifts.append(Shift(thu_closing_shift, day, day + delta))
            else:
                shifts.append(Shift(closing_shift, day, day + delta))


def test_all_constraints():
    test_employee = Employee("test", EmployeePriorityEnum.LOW, EmployeeStatusEnum.new_employee, 1)
    test_employee1 = Employee("test1", EmployeePriorityEnum.LOWEST, EmployeeStatusEnum.new_employee, 2)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 3)
    test_employee3 = Employee("test3", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 4)
    test_employee4 = Employee("test4", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 5)

    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(17, 0), datetime.time(22, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(19, 30), datetime.time(2, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 14))
    test_shift4 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 14), datetime.date(2023, 11, 14))
    test_shift5 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(17, 0), datetime.time(22, 0)), datetime.date(2023, 11, 14), datetime.date(2023, 11, 14))
    test_shift6 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(19, 30), datetime.time(2, 0)), datetime.date(2023, 11, 14), datetime.date(2023, 11, 15))
    test_shift7 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 15), datetime.date(2023, 11, 15))
    test_shift8 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(17, 0), datetime.time(22, 0)), datetime.date(2023, 11, 15), datetime.date(2023, 11, 15))
    test_shift9 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(19, 30), datetime.time(2, 0)), datetime.date(2023, 11, 15), datetime.date(2023, 11, 16))

    employees = [test_employee, test_employee1, test_employee2, test_employee3, test_employee4]
    shift_this_week = [test_shift1, test_shift2, test_shift3, test_shift4, test_shift5, test_shift6, test_shift7, test_shift8, test_shift9]

    model = cp_model.CpModel()
    shifts = generate_shift_employee_combinations(employees, shift_this_week, model)

    add_one_employee_per_shift_constraint(shift_this_week, employees, model, shifts)
    add_at_most_one_shift_in_the_same_day_constraint(shift_this_week, employees, model, shifts)
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, shift_this_week, employees, model, shifts)
    add_no_morning_shift_after_closing_shift_constraint(shift_this_week, employees, model, shifts, timedelta(hours=12))
    add_max_working_days_a_week_constraint(shift_this_week, employees, model, shifts, 2)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)

    # printing to see that the solution is satisfying all the constraints
    for shift in shift_this_week:
        for employee in employees:
            if solver.Value(shifts[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift.value)]):
                print(employee.id, employee.status.value, shift.shift_type.name_of_shift.value, shift.get_str_start_date())


def test_all_constraints2():
    shift_this_week = []

    generate_sun_to_sat_shifts_for_test(datetime.date(2023, 11, 5), datetime.date(2023, 11, 11), shift_this_week)

    # If I am leaving only 2 employees, there is no optimal solution because of the constraint
    # that prevents an employee to work more than one shift that starts on the same day.

    employee1 = Employee("Emily", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    employee2 = Employee("John", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 2)
    employee3 = Employee("Michael", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 3)
    employee4 = Employee("William", EmployeePriorityEnum.MEDIUM, EmployeeStatusEnum.senior_employee, 4)
    employee5 = Employee("Dow", EmployeePriorityEnum.MEDIUM, EmployeeStatusEnum.junior_employee, 5)

    employees = [employee1, employee2, employee3, employee4, employee5]

    max_working_days_in_a_week = 6

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shift_this_week, model)
    add_one_employee_per_shift_constraint(shift_this_week, employees, model, all_shifts)
    add_at_most_one_shift_in_the_same_day_constraint(shift_this_week, employees, model, all_shifts)
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING,
                                                          shift_this_week, employees, model, all_shifts)
    add_no_morning_shift_after_closing_shift_constraint(shift_this_week, employees, model, all_shifts,
                                                        timedelta(hours=12))
    add_max_working_days_a_week_constraint(shift_this_week, employees, model, all_shifts, max_working_days_in_a_week)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    schedule_shifts = []
    for shift in shift_this_week:
        for employee in employees:
            if solver.Value(all_shifts[(
                    employee.id, shift.get_str_start_date(),
                    shift.get_str_end_date(),
                    shift.shift_type.name_of_shift.value)]):
                schedule_shifts.append([shift, employee])
                break
    schedule = WorkersWeekSchedule(schedule_shifts)

    # printing to see that the solution is satisfying all the constraints
    print("")
    for pair in schedule.week_schedule:
        shift_index = 0
        employee_index = 1
        print(
            f"{pair[shift_index].shift_type.name_of_shift.value} shift, starts at {pair[shift_index].start_date_of_shift}, ends at {pair[shift_index].end_date_of_shift}, worked by {pair[employee_index].name}")
        if pair[shift_index].shift_type == ShiftTypesEnum.CLOSING:
            print()
