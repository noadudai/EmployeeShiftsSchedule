import datetime
import uuid

from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum

sunday = [Shift(shift_id="sunday_morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 28, 9, 30), end_time=datetime.datetime(2024, 4, 28, 16)),
          Shift(shift_id="sunday_morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 28, 10, 30), end_time=datetime.datetime(2024, 4, 28, 16)),
          Shift(shift_id="sunday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 28, 16), end_time=datetime.datetime(2024, 4, 29, 0)),
          Shift(shift_id="sunday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 28, 19, 30), end_time=datetime.datetime(2024, 4, 29, 2)),
          Shift(shift_id="sunday_stand_by", shift_type=ShiftTypesEnum.STAND_BY, start_time=datetime.datetime(2024, 4, 28, 20), end_time=datetime.datetime(2024, 4, 29, 2))]
monday = [Shift(shift_id="monday_morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 29, 9, 30), end_time=datetime.datetime(2024, 4, 29, 16)),
          Shift(shift_id="monday_morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 29, 10, 30), end_time=datetime.datetime(2024, 4, 29, 16)),
          Shift(shift_id="monday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 29, 16), end_time=datetime.datetime(2024, 4, 30, 0)),
          Shift(shift_id="monday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 29, 19, 30), end_time=datetime.datetime(2024, 4, 30, 2)),
          Shift(shift_id="monday_stand_by", shift_type=ShiftTypesEnum.STAND_BY, start_time=datetime.datetime(2024, 4, 29, 20), end_time=datetime.datetime(2024, 4, 30, 2))]
tuesday = [Shift(shift_id="tuesday_morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 30, 9, 30), end_time=datetime.datetime(2024, 4, 30, 16)),
           Shift(shift_id="tuesday_morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 30, 10, 30), end_time=datetime.datetime(2024, 4, 30, 16)),
           Shift(shift_id="tuesday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 30, 16), end_time=datetime.datetime(2024, 5, 1, 0)),
           Shift(shift_id="tuesday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 30, 19, 30), end_time=datetime.datetime(2024, 5, 1, 2)),
           Shift(shift_id="tuesday_stand_by", shift_type=ShiftTypesEnum.STAND_BY, start_time=datetime.datetime(2024, 4, 30, 20), end_time=datetime.datetime(2024, 5, 1, 2))]
wednesday = [Shift(shift_id="wednesday_morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 5, 1, 9, 30), end_time=datetime.datetime(2024, 5, 1, 16)),
             Shift(shift_id="wednesday_morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 1, 10, 30), end_time=datetime.datetime(2024, 5, 1, 16)),
             Shift(shift_id="wednesday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 1, 16), end_time=datetime.datetime(2024, 5, 2, 0)),
             Shift(shift_id="wednesday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 1, 19, 30), end_time=datetime.datetime(2024, 5, 2, 2))]
thursday = [Shift(shift_id="thursday_morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 5, 2, 9, 30), end_time=datetime.datetime(2024, 5, 2, 16)),
            Shift(shift_id="thursday_morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 2, 10, 30), end_time=datetime.datetime(2024, 5, 2, 16)),
            Shift(shift_id="thursday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 2, 16), end_time=datetime.datetime(2024, 5, 3, 0)),
            Shift(shift_id="thursday_backup", shift_type=ShiftTypesEnum.THURSDAY_BACKUP, start_time=datetime.datetime(2024, 5, 2, 19, 30), end_time=datetime.datetime(2024, 5, 3, 2)),
            Shift(shift_id="thursday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 2, 21, 30), end_time=datetime.datetime(2024, 5, 3, 2))]
friday = [Shift(shift_id="friday_weekend_morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 5, 3, 7, 30), end_time=datetime.datetime(2024, 5, 3, 14, 30)),
          Shift(shift_id="friday_weekend_morning_backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 3, 8), end_time=datetime.datetime(2024, 5, 3, 17)),
          Shift(shift_id="friday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 3, 16, 30), end_time=datetime.datetime(2024, 5, 4, 0)),
          Shift(shift_id="friday_weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 5, 3, 21, 30), end_time=datetime.datetime(2024, 5, 4, 2)),
          Shift(shift_id="friday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 3, 22), end_time=datetime.datetime(2024, 5, 4, 2))]
saturday = [Shift(shift_id="saturday_weekend_morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 5, 4, 7, 30), end_time=datetime.datetime(2024, 5, 4, 14, 30)),
            Shift(shift_id="saturday_weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 4, 8), end_time=datetime.datetime(2024, 5, 4, 17)),
            Shift(shift_id="saturday_evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 4, 16, 30), end_time=datetime.datetime(2024, 5, 5, 0)),
            Shift(shift_id="saturday_weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 5, 4, 21, 30), end_time=datetime.datetime(2024, 5, 5, 2)),
            Shift(shift_id="saturday_closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 4, 22), end_time=datetime.datetime(2024, 5, 5, 2))]

all_shifts_in_the_week = sunday + monday + tuesday + wednesday + thursday + friday + saturday
