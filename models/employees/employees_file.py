import datetime

from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_preferences.day_preference import DayOffPreference
from models.employees.employee_preferences.preferences import Preferences
from models.employees.employee_preferences.shifts_preference import ShiftsPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shifts_types_enum import ShiftTypesEnum

employee1s_preferences = Preferences(shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2023, 4, 28), [ShiftTypesEnum.MORNING, ShiftTypesEnum.STAND_BY]),
                                                              ShiftsPreference(datetime.date(2024, 4, 29), [ShiftTypesEnum.MORNING]),
                                                              ShiftsPreference(datetime.date(2024, 4, 30), [ShiftTypesEnum.STAND_BY]),
                                                              ShiftsPreference(datetime.date(2024, 5, 1), [ShiftTypesEnum.MORNING_BACKUP]),
                                                              ShiftsPreference(datetime.date(2024, 5, 2), [ShiftTypesEnum.EVENING]),
                                                              ShiftsPreference(datetime.date(2024, 5, 3), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.EVENING]),
                                                              ShiftsPreference(datetime.date(2024, 5, 4), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.EVENING])])

employee2s_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 28)),
                                                 DayOffPreference(datetime.date(2024, 5, 3))])

employee3s_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 28))],
                                 shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 5, 2), [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP]),
                                                                ShiftsPreference(datetime.date(2024, 5, 3), [ShiftTypesEnum.EVENING, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.CLOSING])])

employee4s_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 5, 2)),
                                                  DayOffPreference(datetime.date(2024, 5, 3)),
                                                  DayOffPreference(datetime.date(2024, 5, 4))])

employee5s_preferences = Preferences(days_cannot_work=[DayOffPreference(datetime.date(2024, 5, 1))],
                                   shifts_prefer_to_work_in_days=[ShiftsPreference(datetime.date(2024, 5, 2), [ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING]),
                                                                  ShiftsPreference(datetime.date(2024, 5, 4), [ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP])])

employee6s_preferences = Preferences(days_prefer_not_to_work=[DayOffPreference(datetime.date(2024, 4, 30))],
                                  days_cannot_work=[DayOffPreference(datetime.date(2024, 4, 28)),
                                                    DayOffPreference(datetime.date(2024, 4, 29))])

employee1s_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.STAND_BY]
employee2s_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee3s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee4s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee5s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee6s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]


employee1 = Employee(name="employee1", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="employee1", preferences=employee1s_preferences, shift_types_trained_to_do=employee1s_trained_shifts)
employee2 = Employee(name="employee2", employee_id="employee2", position= EmployeePositionEnum.part_timer, preferences=employee2s_preferences, shift_types_trained_to_do=employee2s_trained_shifts)
employee3 = Employee(name="employee3", employee_id="employee3", preferences=employee3s_preferences, shift_types_trained_to_do=employee3s_trained_shifts)
employee4 = Employee(name="employee4", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="employee4", preferences=employee4s_preferences, shift_types_trained_to_do=employee4s_trained_shifts)
employee5 = Employee(name="employee5", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="employee5", preferences=employee5s_preferences, shift_types_trained_to_do=employee5s_trained_shifts)
employee6 = Employee(name="employee6", employee_id="employee6", position= EmployeePositionEnum.part_timer, preferences=employee6s_preferences, shift_types_trained_to_do=employee6s_trained_shifts)


all_employees = [employee1, employee4, employee5, employee3, employee6, employee2]
