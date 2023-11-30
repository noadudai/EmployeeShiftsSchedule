import datetime
import collections
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


def test_add_one_employee_per_shift_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    test_shift = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    model = cp_model.CpModel()

    shifts = generate_shift_employee_combinations([test_employee, test_employee2], [test_shift], model)
    add_one_employee_per_shift_constraint([test_shift], [test_employee, test_employee2], model, shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # the second employee does not work in the same shift as the first employee, it chose the first employee to
    # work that shift because he is the first value in the given employee list
    start_shift = test_shift.get_str_start_date()
    end_shift = test_shift.get_str_end_date()
    shift_type = test_shift.shift_type.name_of_shift

    assert (status == cp_model.OPTIMAL)

    second_employee_assignment = shifts[(test_employee2.id, start_shift, end_shift, shift_type)]
    assert (solver.Value(second_employee_assignment) == 0)


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

    for shift in [test_shift1, test_shift2, test_shift3]:
        for employee in [test_employee, test_employee2]:
            working_assignment = shifts[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)]
            # the employee does not work this shift
            assert (solver.Value(working_assignment) == 0)


def test_add_at_most_one_shift_in_the_same_day_constraint_with_at_least_one_employee_in_a_shift():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)
    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(9, 30), datetime.time(16, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(16, 0), datetime.time(22, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))

    shifts = [test_shift1, test_shift2, test_shift3]
    employees = [test_employee, test_employee2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    # When adding the constraint "add_one_employee_per_shift_constraint", it also ensures that there is at least one
    # employee in each shift, causing "add_at_most_one_shift_in_the_same_day_constraint" to fail- because the solver
    # needs to assign at least one employee in each shift, and cannot assign an employee to more than 1 shift a day.
    add_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_at_most_one_shift_in_the_same_day_constraint(shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert (status != cp_model.OPTIMAL)


def test_add_prevent_new_employees_working_together_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 2)
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.EVENING, datetime.time(16, 0), datetime.time(22, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 12))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))

    employees = [test_employee, test_employee2]
    shifts = [test_shift2, test_shift3]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, [test_shift2, test_shift3], model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint(shifts, employees,model, all_shifts)
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, shifts, employees, model, all_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # 2 new employees, because of the "add_one_employee_per_shift_constraint" that ensures that there is at least one
    # employee in each shift, there is no optimal solution.
    assert (status != cp_model.OPTIMAL)


def test_add_no_morning_shift_after_closing_shift_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)
    test_employee2 = Employee("test2", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.senior_employee, 2)

    test_shift2 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))

    employees = [test_employee, test_employee2]
    shifts = [test_shift2, test_shift3]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_no_morning_shift_after_closing_shift_constraint(shifts, employees, model, all_shifts, timedelta(hours=12))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    schedule_shifts = []
    for shift in shifts:
        for employee in employees:

            working_assignment = all_shifts[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)]
            if solver.Value(working_assignment):
                schedule_shifts.append([shift, employee.id])

    for shifts_emps_pairs in itertools.pairwise(schedule_shifts):
        first_pair_in_shifts_emps_pair, second_pair_in_shifts_emps_pair = shifts_emps_pairs

        shift_in_first_pair, emp_in_first_pair = first_pair_in_shifts_emps_pair
        shift_in_second_pair, emp_in_second_pair = second_pair_in_shifts_emps_pair

        if shift_in_first_pair.shift_type.name_of_shift == ShiftTypesEnum.CLOSING:
            assert(emp_in_first_pair != emp_in_second_pair)


def test_add_no_morning_shift_after_closing_shift_constraint_with_one_employee():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)

    test_shift2 = Shift(ShiftType(ShiftTypesEnum.CLOSING, datetime.time(17, 30), datetime.time(2, 0)), datetime.date(2023, 11, 12), datetime.date(2023, 11, 13))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))

    shifts = [test_shift2, test_shift3]
    employees = [test_employee]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    time_between_shifts = datetime.timedelta(hours=12)
    add_no_morning_shift_after_closing_shift_constraint(shifts, employees, model, all_shifts, time_between_shifts)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # failed because there is only one employee, and the time between the closing shift and the morning
    # shift the day after is less than 12 hours
    assert (status != cp_model.OPTIMAL)


# A test to verify if "add_max_working_days_a_week_constraint" alongside with  "add_one_employee_per_shift_constraint"
# fail when there is only one employee for three shifts and the maximum working days should be no more than 2.
def test_add_max_working_days_a_week_constraint_with_3_shifts_1_emp():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)

    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 14), datetime.date(2023, 11, 14))
    test_shift3 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 15), datetime.date(2023, 11, 15))

    employees = [test_employee]
    shifts = [test_shift1, test_shift2, test_shift3]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    max_working_days = 2
    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_max_working_days_a_week_constraint(shifts, employees, model, all_shifts, max_working_days)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status != cp_model.OPTIMAL)


def test_add_max_working_days_a_week_constraint():
    test_employee = Employee("test", EmployeePriorityEnum.HIGHEST, EmployeeStatusEnum.new_employee, 1)

    test_shift1 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 13), datetime.date(2023, 11, 13))
    test_shift2 = Shift(ShiftType(ShiftTypesEnum.MORNING, datetime.time(11, 45), datetime.time(17, 0)), datetime.date(2023, 11, 14), datetime.date(2023, 11, 14))

    employees = [test_employee]
    shifts = [test_shift1, test_shift2]

    model = cp_model.CpModel()
    all_shifts = generate_shift_employee_combinations(employees, shifts, model)

    max_working_days_in_a_week = 2
    # Without "add_one_employee_per_shift_constraint" the solver will not assign an employee to a shift.
    add_one_employee_per_shift_constraint(shifts, employees, model, all_shifts)
    add_max_working_days_a_week_constraint(shifts, employees, model, all_shifts, max_working_days_in_a_week)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    assert (status == cp_model.OPTIMAL)
    schedule_shifts = []
    for shift in shifts:
        for employee in employees:

            working_assignment = all_shifts[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)]
            if solver.Value(working_assignment):
                schedule_shifts.append([shift, employee.id])

    schedule = WorkersWeekSchedule(schedule_shifts)

    dict_schedule = dict(schedule.week_schedule)

    # Count the shift for each employee
    emp_amount_of_shifts_dict = collections.Counter(dict_schedule.values())
    assert (max_working_days_in_a_week >= max(emp_amount_of_shifts_dict.values()))


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
    shift_this_week = []

    generate_sun_to_sat_shifts_for_test(datetime.date(2023, 11, 5), datetime.date(2023, 11, 11), shift_this_week)

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
    add_prevent_new_employees_working_together_constraint(ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, shift_this_week, employees, model, all_shifts)
    add_no_morning_shift_after_closing_shift_constraint(shift_this_week, employees, model, all_shifts, timedelta(hours=12))
    add_max_working_days_a_week_constraint(shift_this_week, employees, model, all_shifts, max_working_days_in_a_week)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Test 1 to check for a valid solution
    assert (status == cp_model.OPTIMAL)
    schedule_shifts = []
    for shift in shift_this_week:
        for employee in employees:
            working_assignment = all_shifts[(employee.id, shift.get_str_start_date(), shift.get_str_end_date(), shift.shift_type.name_of_shift)]
            if solver.Value(working_assignment):
                schedule_shifts.append([shift, employee.id])
    schedule = WorkersWeekSchedule(schedule_shifts)

    dict_schedule = dict(schedule.week_schedule)
    emp_amount_of_shifts_dict = collections.Counter(dict_schedule.values())

    # Test 2 to check if the max days a week constraint is satisfied
    assert (max_working_days_in_a_week >= max(emp_amount_of_shifts_dict.values()))

    for shifts_emps_pairs in itertools.pairwise(schedule.week_schedule):
        first_pair_in_shifts_emps_pair, second_pair_in_shifts_emps_pair = shifts_emps_pairs

        shift_in_first_pair, emp_in_first_pair = first_pair_in_shifts_emps_pair
        shift_in_second_pair, emp_in_second_pair = second_pair_in_shifts_emps_pair

        # Test 3 to check that the closing employee will not do the next shift according to the time diff between
        # the shifts in this test.
        if shift_in_first_pair.shift_type.name_of_shift == ShiftTypesEnum.CLOSING:
            assert (emp_in_first_pair != emp_in_second_pair)

        # Test 4 to check that the evening employee and the closing employee are not both new employees according to the
        # shifts in this test
        if shift_in_first_pair.shift_type.name_of_shift == ShiftTypesEnum.EVENING and shift_in_second_pair.shift_type.name_of_shift == ShiftTypesEnum.CLOSING:
            first_employee = None
            second_employee = None
            for employee in employees:
                if employee.id == emp_in_first_pair:
                    first_employee = employee
                elif employee.id == emp_in_second_pair:
                    second_employee = employee

            if first_employee.status == EmployeeStatusEnum.new_employee:
                assert (second_employee.status != EmployeeStatusEnum.new_employee)
            if second_employee.status == EmployeeStatusEnum.new_employee:
                assert (first_employee.status != EmployeeStatusEnum.new_employee)

