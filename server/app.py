import uuid
import json
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict


from main import create_shift_dictionary_for_html, create_employee_dictionary_for_html, create_schedule_options
from models.employees.employees_file import all_employees
from models.shifts.shifts_file import all_shifts_in_the_week
from static_site.create_schedule_tables import schedule_to_json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def index():
    return {"Hey There"}


@app.get("/create-and-get-schedule-options")
async def create_schedules():
    employees = all_employees
    shifts = all_shifts_in_the_week
    number_of_solutions = 3
    shift_dict = create_shift_dictionary_for_html(shifts)
    emp_dict = create_employee_dictionary_for_html(employees)

    try:
        schedules = create_schedule_options(employees, shifts, number_of_solutions)
        list_of_schedule_options = []
        additional_data: list[dict[str, defaultdict[uuid.UUID, int]]] = []

        for solution in schedules.solutions:
            list_of_schedule_options.append(schedule_to_json(solution.schedule, shifts, employees))
            metadata_for_schedule = {"number_of_shifts": solution.number_of_shift_for_each_emp,
                                     "number_morning_shifts": solution.number_of_mornings_for_each_emp,
                                     "number_closing_shifts": solution.number_of_closings_for_each_emp}
            additional_data.append(metadata_for_schedule)

        json_data = {"schedules": list_of_schedule_options, "employees": emp_dict, "shifts": shift_dict}

        return {"schedules_info": json_data, "additional_data": additional_data}

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=e.args)
