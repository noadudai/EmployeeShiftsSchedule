import itertools
import json
import uuid
from collections import defaultdict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ortools.sat.python import cp_model

from constraints_file import generate_shift_employee_combinations, \
    add_prevent_overlapping_shifts_for_employees_constraint, add_exactly_one_employee_per_shift_constraint, \
    add_aspire_for_minimal_deviation_between_employees_position_and_number_of_shifts_given_constraint, \
    add_employees_can_work_only_shifts_that_they_trained_for_constraint, \
    add_aspire_to_maximize_all_employees_preferences_constraint
from models.employees.employees_file import all_employees
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_file import all_shifts_in_the_week
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.solution.create_solutions import create_solutions
from models.solution.one_schedule_solution_metadata import ScheduleSolutionMetadata
from models.solution.schedule_solutions import ScheduleSolutions
from models.solution.schedules_and_emps_metadata import SchedulesAndEmpsMetadata

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
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

@app.get("/create_and_get_schedule_options", response_model=SchedulesAndEmpsMetadata)
async def create_and_get_schedule_options():
    employees = all_employees
    shifts = all_shifts_in_the_week

    schedule_solution: ScheduleSolutions = create_solutions(employees, shifts)

    schedules_options = []
    for i in itertools.islice(schedule_solution.yield_schedules(), 100):
        schedules_options.append(i)

    metadata = SchedulesAndEmpsMetadata(schedules_options, employees, shifts)

    return metadata
