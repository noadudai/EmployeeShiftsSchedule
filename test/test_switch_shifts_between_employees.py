from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint, \
    add_an_employees_switch_shifts_after_schedule_created_constraint
from main import create_a_new_schedule
from models.employees.employee_preferences.emps_shifts_switch import EmployeesShiftsSwitch
from models.employees.employees_file import all_employees
from models.shifts.shifts_file import all_shifts_in_the_week


def test_2_employees_can_switch_shifts():
    employees = all_employees
    shifts = all_shifts_in_the_week

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()

    print("Creating schedules")
    status = solver.Solve(constraint_model)
    assert (status == cp_model.OPTIMAL)

    solution = create_a_new_schedule(solver, all_shifts, employees, shifts)

    assert (solution.schedule["monday_evening"] == "employee5")
    assert (solution.schedule["monday_closing"] == "employee4")

    # taken hard coded from the schedule output when solved.
    emps_who_wants_to_switch = EmployeesShiftsSwitch(emp_who_wnats_to_switch_id="employee5", emp_who_wnats_to_switch_has_shift="monday_evening", emp_who_wnats_to_switch_wants_shift="monday_closing", emp_to_switch_with_id="employee4", emp_to_switch_with_has_shift="monday_closing", emp_to_switch_with_wants_shift="monday_evening")

    result = add_an_employees_switch_shifts_after_schedule_created_constraint(constraint_model, emps_who_wants_to_switch, solver, all_shifts, employees, shifts)

    assert (result != False)

    assert (result.schedule["monday_evening"] == "employee4")
    assert (result.schedule["monday_closing"] == "employee5")

    print("done")


def test_2_employees_cannot_switch_shifts_because_one_of_the_employees_is_not_trained_to_do_the_switched_shift():
    employees = all_employees
    shifts = all_shifts_in_the_week

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees,
                                                                                                      constraint_model,
                                                                                                      all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()

    print("Creating schedules")
    status = solver.Solve(constraint_model)
    assert (status == cp_model.OPTIMAL)

    solution = create_a_new_schedule(solver, all_shifts, employees, shifts)

    # should be in the schedule, since employee1 is the highest employee and wants to work the evening
    # taken hard coded from the schedule output when solved.
    if solution.schedule["thursday_evening"] == "employee1" and solution.schedule["thursday_backup"] == "employee3":
        emps_who_wants_to_switch = EmployeesShiftsSwitch(emp_who_wnats_to_switch_id="employee3",
                                                         emp_who_wnats_to_switch_has_shift="thursday_backup",
                                                         emp_who_wnats_to_switch_wants_shift="thursday_evening",
                                                         emp_to_switch_with_id="employee1",
                                                         emp_to_switch_with_has_shift="thursday_evening",
                                                         emp_to_switch_with_wants_shift="thursday_backup")

    result = add_an_employees_switch_shifts_after_schedule_created_constraint(constraint_model,
                                                                              emps_who_wants_to_switch, solver,
                                                                              all_shifts, employees, shifts)

    assert (result == False)
    print("done")


def test_2_employees_switch_shifts_even_when_its_a_shift_the_employee_wanted():
    employees = all_employees
    shifts = all_shifts_in_the_week

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees,
                                                                                                      constraint_model,
                                                                                                      all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()

    print("Creating schedules")
    status = solver.Solve(constraint_model)
    assert (status == cp_model.OPTIMAL)

    solution = create_a_new_schedule(solver, all_shifts, employees, shifts)

    # employee5 wanted to work evening/backup/closing on thursday, received a closing shift. employee3 wants to close instead
    # taken hard coded from the schedule output when solved.
    if solution.schedule["thursday_closing"] == "employee5" and solution.schedule["thursday_backup"] == "employee3":
        emps_who_wants_to_switch = EmployeesShiftsSwitch(emp_who_wnats_to_switch_id="employee5",
                                                         emp_who_wnats_to_switch_has_shift="thursday_closing",
                                                         emp_who_wnats_to_switch_wants_shift="thursday_backup",
                                                         emp_to_switch_with_id="employee3",
                                                         emp_to_switch_with_has_shift="thursday_backup",
                                                         emp_to_switch_with_wants_shift="thursday_closing")

    result = add_an_employees_switch_shifts_after_schedule_created_constraint(constraint_model,
                                                                              emps_who_wants_to_switch, solver,
                                                                              all_shifts, employees, shifts)

    assert (result.schedule["thursday_closing"] == "employee3")
    assert (result.schedule["thursday_backup"] == "employee5")
    print("done")
