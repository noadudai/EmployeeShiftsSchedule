import json

from constraints_file import *
from models.employees.employee import Employee
from models.employees.employees_file import all_employees
from models.shifts.shift import Shift
from models.shifts.shifts_file import all_shifts_in_the_week
from models.solution.create_solutions import create_solutions
from models.solution.schedule_solutions import ScheduleSolutions
from static_site.create_schedule_tables import schedule_to_json


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
    number_of_solutions = 10
    shift_dict = create_shift_dictionary_for_html(shifts)
    emp_dict = create_employee_dictionary_for_html(employees)

    try:
        schedule_solution: ScheduleSolutions = create_solutions(employees, shifts)
        json_schedule_options = []

        schedules_options = []
        for i in itertools.islice(schedule_solution.yield_schedules(), 5):
            schedules_options.append(i)

        for solution in schedules_options:
            json_schedule_options.append(schedule_to_json(solution.schedule, shifts, employees))

        json_data = {"schedules": json_schedule_options, "employees": emp_dict, "shifts": shift_dict}
        with open("static_site/schedule_data.json", "w") as json_data_file:
            json.dump(json_data, json_data_file)

    except Exception as e:
        print(e)
