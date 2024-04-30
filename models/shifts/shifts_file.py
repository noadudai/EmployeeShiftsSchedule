import datetime
import uuid

from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum

sunday = [Shift(shift_id="2024, 4, 28,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 28, 9, 30), end_time=datetime.datetime(2024, 4, 28, 16)),
          Shift(shift_id="2024, 4, 28,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 28, 10, 30), end_time=datetime.datetime(2024, 4, 28, 16)),
          Shift(shift_id="2024, 4, 28,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 28, 16), end_time=datetime.datetime(2024, 4, 29, 0)),
          Shift(shift_id="2024, 4, 28,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 28, 19, 30), end_time=datetime.datetime(2024, 4, 29, 2)),
          Shift(shift_id="2024, 4, 28, stand_by", shift_type=ShiftTypesEnum.STAND_BY, start_time=datetime.datetime(2024, 4, 28, 20), end_time=datetime.datetime(2024, 4, 29, 2))]
monday = [Shift(shift_id="2024, 4, 29,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 29, 9, 30), end_time=datetime.datetime(2024, 4, 29, 16)),
          Shift(shift_id="2024, 4, 29,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 29, 10, 30), end_time=datetime.datetime(2024, 4, 29, 16)),
          Shift(shift_id="2024, 4, 29,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 29, 16), end_time=datetime.datetime(2024, 4, 30, 0)),
          Shift(shift_id="2024, 4, 29,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 29, 19, 30), end_time=datetime.datetime(2024, 4, 30, 2)),
          Shift(shift_id="2024, 4, 29, stand_by", shift_type=ShiftTypesEnum.STAND_BY, start_time=datetime.datetime(2024, 4, 29, 20), end_time=datetime.datetime(2024, 4, 30, 2))]
tuesday = [Shift(shift_id="2024, 4, 30,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 30, 9, 30), end_time=datetime.datetime(2024, 4, 30, 16)),
           Shift(shift_id="2024, 4, 30,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 30, 10, 30), end_time=datetime.datetime(2024, 4, 30, 16)),
           Shift(shift_id="2024, 4, 30,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 30, 16), end_time=datetime.datetime(2024, 5, 1, 0)),
           Shift(shift_id="2024, 4, 30,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 30, 19, 30), end_time=datetime.datetime(2024, 5, 1, 2)),
          Shift(shift_id="2024, 4, 30, stand_by", shift_type=ShiftTypesEnum.STAND_BY, start_time=datetime.datetime(2024, 4, 30, 20), end_time=datetime.datetime(2024, 5, 1, 2))]
wednesday = [Shift(shift_id="2024, 5, 1,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 5, 1, 9, 30), end_time=datetime.datetime(2024, 5, 1, 16)),
             Shift(shift_id="2024, 5, 1,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 1, 10, 30), end_time=datetime.datetime(2024, 5, 1, 16)),
             Shift(shift_id="2024, 5, 1,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 1, 16), end_time=datetime.datetime(2024, 5, 2, 0)),
             Shift(shift_id="2024, 5, 1,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 1, 19, 30), end_time=datetime.datetime(2024, 5, 2, 2))]
thursday = [Shift(shift_id="2024, 5, 2,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 5, 2, 9, 30), end_time=datetime.datetime(2024, 5, 2, 16)),
            Shift(shift_id="2024, 5, 2,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 2, 10, 30), end_time=datetime.datetime(2024, 5, 2, 16)),
            Shift(shift_id="2024, 5, 2,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 2, 16), end_time=datetime.datetime(2024, 5, 3, 0)),
            Shift(shift_id="2024, 5, 2,thursday_backup", shift_type=ShiftTypesEnum.THURSDAY_BACKUP, start_time=datetime.datetime(2024, 5, 2, 19, 30), end_time=datetime.datetime(2024, 5, 3, 2)),
            Shift(shift_id="2024, 5, 2,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 2, 21, 30), end_time=datetime.datetime(2024, 5, 3, 2))]
friday = [Shift(shift_id="2024, 5, 3,weekend_morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 5, 3, 7, 30), end_time=datetime.datetime(2024, 5, 3, 14, 30)),
          Shift(shift_id="2024, 5, 3,weekend_morning_backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 3, 8), end_time=datetime.datetime(2024, 5, 3, 17)),
          Shift(shift_id="2024, 5, 3,weekend_morning_backup2", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 3, 11, 30), end_time=datetime.datetime(2024, 5, 3, 19)),
          Shift(shift_id="2024, 5, 3,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 3, 16, 30), end_time=datetime.datetime(2024, 5, 4, 0)),
          Shift(shift_id="2024, 5, 3,weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 5, 3, 21, 30), end_time=datetime.datetime(2024, 5, 4, 2)),
          Shift(shift_id="2024, 5, 3,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 3, 22), end_time=datetime.datetime(2024, 5, 4, 2))]
saturday = [Shift(shift_id="2024, 5, 4,weekend_morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 5, 4, 7, 30), end_time=datetime.datetime(2024, 5, 4, 14, 30)),
            Shift(shift_id="2024, 5, 4,weekend_morning_backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 4, 8), end_time=datetime.datetime(2024, 5, 4, 17)),
            Shift(shift_id="2024, 5, 4,weekend_morning_backup2", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 5, 4, 11, 30), end_time=datetime.datetime(2024, 5, 4, 19)),
            Shift(shift_id="2024, 5, 4,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 5, 4, 16, 30), end_time=datetime.datetime(2024, 5, 5, 0)),
            Shift(shift_id="2024, 5, 4,weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 5, 4, 21, 30), end_time=datetime.datetime(2024, 5, 5, 2)),
            Shift(shift_id="2024, 5, 4,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 5, 4, 22), end_time=datetime.datetime(2024, 5, 5, 2))]

all_shifts_in_the_week = sunday + monday + tuesday + wednesday + thursday + friday + saturday
