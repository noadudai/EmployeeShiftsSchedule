from ortools.sat.python import cp_model

from src.constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint
from src.models.employees.employee import Employee
from src.models.shifts.shift import Shift
from src.models.solution.schedule_solutions import ScheduleSolutions


def create_solutions(employees: list[Employee], shifts: list[Shift]) -> ScheduleSolutions:

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()

    my_solution = ScheduleSolutions(solver, all_shifts, employees, shifts, constraint_model)

    return my_solution
