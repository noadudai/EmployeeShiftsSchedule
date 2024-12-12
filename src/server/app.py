import itertools

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models.employees.employees_file import all_employees
from src.models.shifts.shifts_file import all_shifts_in_the_week
from src.models.solution.create_solutions import create_solutions
from src.models.solution.schedule_solutions import ScheduleSolutions
from src.models.solution.schedules_and_emps_metadata import SchedulesAndEmpsMetadata

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
