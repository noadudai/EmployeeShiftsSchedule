import json

import uvicorn

from src.constraints_file import *
from src.models.employees.employee import Employee
from src.models.employees.employees_file import all_employees
from src.models.shifts.shift import Shift
from src.models.shifts.shifts_file import all_shifts_in_the_week
from src.models.solution.create_solutions import create_solutions
from src.models.solution.schedule_solutions import ScheduleSolutions
from src.server.app import app
from src.static_site.create_schedule_tables import schedule_to_json


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


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8007)