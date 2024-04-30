import datetime

from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_preferences.day_preference import DayOffPreference
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shifts_types_enum import ShiftTypesEnum

noas_preferences = Preferences(shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2023, 4, 28), [ShiftTypesEnum.MORNING, ShiftTypesEnum.STAND_BY]),
                                                              ShiftsPreference(datetime.date(2024, 4, 29), [ShiftTypesEnum.MORNING]),
                                                              ShiftsPreference(datetime.date(2024, 4, 30), [ShiftTypesEnum.STAND_BY]),
                                                              ShiftsPreference(datetime.date(2024, 5, 1), [ShiftTypesEnum.MORNING_BACKUP]),
                                                              ShiftsPreference(datetime.date(2024, 5, 2), [ShiftTypesEnum.EVENING]),
                                                              ShiftsPreference(datetime.date(2024, 5, 3), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.EVENING]),
                                                              ShiftsPreference(datetime.date(2024, 5, 4), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.EVENING])])

tals_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 28)),
                                                 DayOffPreference(datetime.date(2024, 5, 3))])

yossis_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 28))],
                                 shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 5, 2), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                                                ShiftsPreference(datetime.date(2024, 5, 3), [ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING])])

lavis_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 5, 2)),
                                                  DayOffPreference(datetime.date(2024, 5, 3)),
                                                  DayOffPreference(datetime.date(2024, 5, 4))])

pinchass_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 5, 1))],
                                   shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 5, 2), [ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING]),
                                                                  ShiftsPreference(datetime.date(2024, 5, 4), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

shellys_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 30))],
                                  days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 28)),
                                                    DayOffPreference(datetime.date(2024, 4, 29))])

noas_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.STAND_BY]
tals_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
yossis_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
lavis_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
pinchass_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
shellys_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]


noa = Employee(name="Noa", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Noa", preferences=noas_preferences, shift_types_trained_to_do=noas_trained_shifts)
tal = Employee(name="Tal", employee_id="Tal", position= EmployeePositionEnum.part_timer, preferences=tals_preferences, shift_types_trained_to_do=tals_trained_shifts)
yossi = Employee(name="Yossi", employee_id="Yossi", preferences=yossis_preferences, shift_types_trained_to_do=yossis_trained_shifts)
lavi = Employee(name="Lavi", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Lavi", preferences=lavis_preferences, shift_types_trained_to_do=lavis_trained_shifts)
pinchas = Employee(name="Pinchas", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="Pinchas", preferences=pinchass_preferences, shift_types_trained_to_do=pinchass_trained_shifts)
shelly = Employee(name="Shelly", employee_id="Shelly", position= EmployeePositionEnum.part_timer, preferences=shellys_preferences, shift_types_trained_to_do=shellys_trained_shifts)


this_weeks_employees = [noa, lavi, pinchas, yossi, shelly, tal]
