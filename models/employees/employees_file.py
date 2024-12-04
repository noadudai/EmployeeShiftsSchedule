import datetime

from models.employees.employee import Employee
from models.employees.employee_position_enum import EmployeePositionEnum
from models.employees.employee_preferences.combine_preference import CombinePreference
from models.employees.employee_preferences.employees_shifts_preferences import EmployeesShiftsPreferences
from models.employees.employee_preferences.date_time_range_preference_ import DateTimeRangePreference
from models.employees.employee_preferences.shifts_preference_by_id import ShiftIdPreference
from models.employees.employee_priority_enum import EmployeePriorityEnum
from models.employees.employee_status_enum import EmployeeStatusEnum
from models.shifts.shifts_types_enum import ShiftTypesEnum

employee1s_preferences = EmployeesShiftsPreferences(shifts_wants_to_work=ShiftIdPreference(["sunday_morning", "sunday_sb", "monday_morning", "tuesday_sb", "wednesday_morning_backup",
                                                                               "thursday_evening","friday_weekend_morning", "friday_evening", "saturday_weekend_morning", "saturday_evening"]))

employee2s_preferences = EmployeesShiftsPreferences(shifts_cannot_work=CombinePreference([DateTimeRangePreference(datetime.datetime(2024, 4, 28, 6), datetime.datetime(2024, 4, 28, 23, 59)),
                                                                                          DateTimeRangePreference(datetime.datetime(2024, 5, 3, 6), datetime.datetime(2024, 5, 3, 23, 59))]))

employee3s_preferences = EmployeesShiftsPreferences(shifts_cannot_work=DateTimeRangePreference(datetime.datetime(2024, 4, 28, 6), datetime.datetime(2024, 4, 28, 23, 59)),
                                                    shifts_wants_to_work=ShiftIdPreference(["thursday_morning", "thursday_morning_backup", "friday_evening", "friday_weekend_evening_backup", "friday_closing"]))

employee4s_preferences = EmployeesShiftsPreferences(shifts_cannot_work=DateTimeRangePreference(datetime.datetime(2024, 5, 2, 00), datetime.datetime(2024, 5, 4, 23, 59)))

employee5s_preferences = EmployeesShiftsPreferences(shifts_cannot_work=DateTimeRangePreference(datetime.datetime(2024, 5, 1, 6), datetime.datetime(2024, 5, 2, 23, 59)),
                                                    shifts_wants_to_work=ShiftIdPreference(["thursday_evening", "thursday_backup", "thursday_closing", "saturday_weekend_morning", "saturday_weekend_morning_backup"]))

employee6s_preferences = EmployeesShiftsPreferences(shifts_prefer_not_to_work=DateTimeRangePreference(datetime.datetime(2024, 4, 30, 6), datetime.datetime(2024, 4, 30, 23, 59)),
                                                    shifts_cannot_work=DateTimeRangePreference(datetime.datetime(2024, 4, 28, 00), datetime.datetime(2024, 4, 29, 23, 59)))

employee1s_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.STAND_BY]
employee2s_trained_shifts = [ShiftTypesEnum.EVENING, ShiftTypesEnum.CLOSING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee3s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee4s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee5s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.EVENING, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]
employee6s_trained_shifts = [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP, ShiftTypesEnum.THURSDAY_BACKUP, ShiftTypesEnum.CLOSING, ShiftTypesEnum.WEEKEND_MORNING, ShiftTypesEnum.WEEKEND_MORNING_BACKUP, ShiftTypesEnum.WEEKEND_EVENING_BACKUP, ShiftTypesEnum.STAND_BY]


employee1 = Employee(name="employee1", priority=EmployeePriorityEnum.HIGHEST, employee_status=EmployeeStatusEnum.senior_employee, employee_id="employee1", shifts_preferences=employee1s_preferences, shift_types_trained_to_do=employee1s_trained_shifts)
employee2 = Employee(name="employee2", employee_id="employee2", position= EmployeePositionEnum.part_timer, shifts_preferences=employee2s_preferences, shift_types_trained_to_do=employee2s_trained_shifts)
employee3 = Employee(name="employee3", employee_id="employee3", shifts_preferences=employee3s_preferences, shift_types_trained_to_do=employee3s_trained_shifts)
employee4 = Employee(name="employee4", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="employee4", shifts_preferences=employee4s_preferences, shift_types_trained_to_do=employee4s_trained_shifts)
employee5 = Employee(name="employee5", priority=EmployeePriorityEnum.HIGH, employee_status=EmployeeStatusEnum.senior_employee, employee_id="employee5", shifts_preferences=employee5s_preferences, shift_types_trained_to_do=employee5s_trained_shifts)
employee6 = Employee(name="employee6", employee_id="employee6", position= EmployeePositionEnum.part_timer, shifts_preferences=employee6s_preferences, shift_types_trained_to_do=employee6s_trained_shifts)


all_employees = [employee1, employee4, employee5, employee3, employee6, employee2]
