from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, add_exactly_one_employee_per_shift_constraint, \
    add_prevent_overlapping_shifts_for_employees_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint
from models.employees.employee import Employee
from models.shifts.shift import Shift
from models.solution.schedule_solutions import ScheduleSolutions


def create_schedule_options(employees: list[Employee], shifts: list[Shift], number_of_solutions: int) -> list:

    constraint_model = cp_model.CpModel()

    all_shifts = generate_shift_employee_combinations(employees, shifts, constraint_model)
    add_exactly_one_employee_per_shift_constraint(shifts, employees, constraint_model, all_shifts)
    add_prevent_overlapping_shifts_for_employees_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint(shifts, employees, constraint_model, all_shifts)
    add_employees_can_work_only_shifts_that_they_trained_for_constraint(shifts, employees, constraint_model, all_shifts)
    add_aspire_to_maximize_all_employees_preferences_constraint(shifts, employees, constraint_model, all_shifts)

    solver = cp_model.CpSolver()

    my_solution = ScheduleSolutions(solver)

    schedules_options = []
    print("Creating schedules")
    for i in range(5):
        schedules_options.append(next(my_solution.yield_schedules(all_shifts, employees, shifts, constraint_model)))

    print("Done")
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
