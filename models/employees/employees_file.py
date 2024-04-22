import datetime

from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_preferences.day_preference import DayOffPreference
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shifts_types_enum import ShiftTypesEnum

noas_preferences = Preferences(shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 23), [ShiftTypesEnum.EVENING])])

bennys_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 22)),
                                                   DayOffPreference(datetime.date(2024, 4, 24)),
                                                   DayOffPreference(datetime.date(2024, 4, 25)),
                                                   DayOffPreference(datetime.date(2024, 4, 26)),
                                                   DayOffPreference(datetime.date(2024, 4, 27))],
                                 shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 21), [ShiftTypesEnum.CLOSING]),
                                                                ShiftsPreference(datetime.date(2024, 4, 23), [ShiftTypesEnum.CLOSING])])

tals_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 26)),
                                                 DayOffPreference(datetime.date(2024, 4, 27))],
                               shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 25), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP])])

yossis_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 23))],
                                 shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 22), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                                                ShiftsPreference(datetime.date(2024, 4, 25), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                                                ShiftsPreference(datetime.date(2024, 4, 26), [ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING])])

lavis_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 22)),
                                                  DayOffPreference(datetime.date(2024, 4, 23))],
                                shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 26), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP]),
                                                               ShiftsPreference(datetime.date(2024, 4, 27), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

idos_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 23)),
                                                 DayOffPreference(datetime.date(2024, 4, 27))],
                               days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 25))],
                               shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 21), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING]),
                                                              ShiftsPreference(datetime.date(2024, 4, 22), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                                              ShiftsPreference(datetime.date(2024, 4, 24), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING]),
                                                              ShiftsPreference(datetime.date(2024, 4, 26), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP])])

pinchass_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 22)),
                                                     DayOffPreference(datetime.date(2024, 4, 23))],
                                   shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 4, 21), [ShiftTypesEnum.CLOSING]),
                                                                  ShiftsPreference(datetime.date(2024, 4, 24), [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING]),
                                                                  ShiftsPreference(datetime.date(2024, 4, 25), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP]),
                                                                  ShiftsPreference(datetime.date(2024, 4, 26), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP]),
                                                                  ShiftsPreference(datetime.date(2024, 4, 27), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP])])

shellys_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 21)),
                                                           DayOffPreference(datetime.date(2024, 4, 22)),
                                                           DayOffPreference(datetime.date(2024, 4, 23)),
                                                           DayOffPreference(datetime.date(2024, 4, 24)),
                                                           DayOffPreference(datetime.date(2024, 4, 25)),
                                                           DayOffPreference(datetime.date(2024, 4, 26)),
                                                           DayOffPreference(datetime.date(2024, 4, 27))])

noas_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.MORNING]
bennys_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]
tals_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]
yossis_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]
lavis_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]
idos_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]
pinchass_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]
shellys_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP]


noa = Employee(name="Noa", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Noa", preferences=noas_preferences, shift_types_trained_to_do=noas_trained_shifts)
benny = Employee(name="Benny", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Benny", preferences=bennys_preferences, shift_types_trained_to_do=bennys_trained_shifts)
tal = Employee(name="Tal", employee_id="Tal", position= EmployeePositionEnum.part_timer, preferences=tals_preferences, shift_types_trained_to_do=tals_trained_shifts)
yossi = Employee(name="Yossi", employee_id="Yossi", preferences=yossis_preferences, shift_types_trained_to_do=yossis_trained_shifts)
lavi = Employee(name="Lavi", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Lavi", preferences=lavis_preferences, shift_types_trained_to_do=lavis_trained_shifts)
ido = Employee(name="Ido", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Ido", preferences=idos_preferences, shift_types_trained_to_do=idos_trained_shifts)
pinchas = Employee(name="Pinchas", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Pinchas", preferences=pinchass_preferences, shift_types_trained_to_do=pinchass_trained_shifts)
shelly = Employee(name="Shelly", employee_id="Shelly", position= EmployeePositionEnum.part_timer, preferences=shellys_preferences, shift_types_trained_to_do=shellys_trained_shifts)


this_weeks_employees = [noa, benny, tal, yossi, lavi, ido, pinchas, shelly]
