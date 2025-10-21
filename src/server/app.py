import itertools

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.client.api_models.schedule_creation_data import ScheduleCreationData
from src.client.converters.employee_converters import api_employee_to_internal_employee
from src.models.solution.create_solutions import create_solutions
from src.models.solution.schedule_solutions import ScheduleSolutions
from src.models.solution.schedules_and_emps_metadata import SchedulesAndEmpsMetadata

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:8007",
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


@app.post("/create_and_get_schedule_options", response_model=SchedulesAndEmpsMetadata)
async def create_and_get_schedule_options(schedule_data: ScheduleCreationData):
    employees = list(api_employee_to_internal_employee(employee) for employee in schedule_data.employees)
    shifts = schedule_data.shifts

    schedule_solution: ScheduleSolutions = create_solutions(employees, shifts)

    schedules_options = []
    for i in itertools.islice(schedule_solution.yield_schedules(), schedule_data.number_of_schedules):
        schedules_options.append(i)

    metadata = SchedulesAndEmpsMetadata(schedules_options, employees, shifts)

    return metadata
