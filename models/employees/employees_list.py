import datetime
import uuid

from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_preferences.day_preference import DayOffPreference
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shifts_types_enum import ShiftTypesEnum

noa_preferences = None

lavi_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(year=2024, month=4, day=12))], shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(year=2024, month=4, day=13), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

pinchas_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(year=2024, month=4, day=9)), DayOffPreference(datetime.date(year=2024, month=4, day=10))], shifts_prefer_to_work_in_days=
[ShiftsPreference(datetime.date(2024, 4, 7), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
 ShiftsPreference(datetime.date(2024, 4, 8), [ShiftTypesEnum.MORNING, ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
 ShiftsPreference(datetime.date(2024, 4, 11), [ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING]),
 ShiftsPreference(datetime.date(2024, 4, 12), [ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING]),
 ShiftsPreference(datetime.date(2024, 4, 13), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING])])

tal_kuzu_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 8))])

tal_uzan_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 12))], days_cannot_work=[DayOffPreference(datetime.date(20024, 4, 13))])

yossi_preferences = Preferences(shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 12), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP]), ShiftsPreference(datetime.date(2024, 4, 13), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

itay_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 13))], shifts_prefer_to_work_in_days=
[ShiftsPreference(datetime.date(2024, 4, 7), [ShiftTypesEnum.MORNING]),
 ShiftsPreference(datetime.date(2024, 4, 8), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
 ShiftsPreference(datetime.date(2024, 4, 12), [ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING])])

rafael_preferences = Preferences(shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 10), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
                                                                ShiftsPreference(datetime.date(2024, 4, 11), [ShiftTypesEnum.MORNING]),
                                                                ShiftsPreference(datetime.date(2024, 4, 13), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING])])

benny_preferences = None

shelly_preferences = Preferences(shifts_prefer_to_work_in_days=[
    ShiftsPreference(datetime.date)])

noa =Employee(name="Noa Dudai", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid.uuid4())
lavi = Employee(name="Lavi Kaosoan", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid.uuid4(), preferences=lavi_preferences)
pinchas = Employee(name="Pinchas Goldman", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid.uuid4(), preferences=pinchas_preferences)
tal_kuzu = Employee(name="Tal Kuzusash", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id=uuid.uuid4(), preferences=tal_kuzu_preferences)
tal_uzan = Employee(name="Tal Uzan", priority=EmployeePriorityEnum.MEDIUM, employee_status=EmployeeStatusEnum.mid_level_employee, employee_id=uuid.uuid4(), position=EmployeePositionEnum.part_timer, preferences=tal_uzan_preferences)
yossi = Employee(name="Yossi Eliyahu", priority=EmployeePriorityEnum.LOW, employee_status=EmployeeStatusEnum.junior_employee, employee_id=uuid.uuid4(), preferences=yossi_preferences)
itay = Employee(name="Itay Haviv", priority=EmployeePriorityEnum.LOW, employee_status=EmployeeStatusEnum.junior_employee, employee_id=uuid.uuid4(), preferences=itay_preferences)
rafael = Employee(name="Rafael Kosovsky", priority=EmployeePriorityEnum.LOWEST, employee_status=EmployeeStatusEnum.new_employee, employee_id=uuid.uuid4(), position=EmployeePositionEnum.part_timer, preferences=rafael_preferences)

