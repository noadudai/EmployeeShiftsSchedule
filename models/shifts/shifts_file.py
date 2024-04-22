import datetime
import uuid

from models.shifts.shift import Shift
from models.shifts.shifts_types_enum import ShiftTypesEnum

sunday = [Shift(shift_id="2024, 4, 21,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 21, 9, 30), end_time=datetime.datetime(2024, 4, 21, 16)),
          Shift(shift_id="2024, 4, 21,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 21, 10, 30), end_time=datetime.datetime(2024, 4, 21, 16)),
          Shift(shift_id="2024, 4, 21,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 21, 16), end_time=datetime.datetime(2024, 4, 22, 0)),
          Shift(shift_id="2024, 4, 21,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 21, 19, 30), end_time=datetime.datetime(2024, 4, 22, 2))]
monday = [Shift(shift_id="2024, 4, 22,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 22, 9, 30), end_time=datetime.datetime(2024, 4, 21, 16)),
          Shift(shift_id="2024, 4, 22,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 22, 10, 30), end_time=datetime.datetime(2024, 4, 21, 16))]
tuesday = [Shift(shift_id="2024, 4, 23,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 23, 9, 30), end_time=datetime.datetime(2024, 4, 23, 16)),
           Shift(shift_id="2024, 4, 23,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 23, 16), end_time=datetime.datetime(2024, 4, 24, 0)),
           Shift(shift_id="2024, 4, 23,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 23, 19, 30), end_time=datetime.datetime(2024, 4, 24, 2))]
wednesday = [Shift(shift_id="2024, 4, 24,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 24, 9, 30), end_time=datetime.datetime(2024, 4, 24, 16)),
             Shift(shift_id="2024, 4, 24,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 24, 10, 30), end_time=datetime.datetime(2024, 4, 24, 16)),
             Shift(shift_id="2024, 4, 24,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 24, 16), end_time=datetime.datetime(2024, 4, 25, 0)),
             Shift(shift_id="2024, 4, 24,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 24, 19, 30), end_time=datetime.datetime(2024, 4, 25, 2))]
thursday = [Shift(shift_id="2024, 4, 25,morning", shift_type=ShiftTypesEnum.MORNING, start_time=datetime.datetime(2024, 4, 25, 9, 30), end_time=datetime.datetime(2024, 4, 25, 16)),
            Shift(shift_id="2024, 4, 25,morning_backup", shift_type=ShiftTypesEnum.MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 25, 10, 30), end_time=datetime.datetime(2024, 4, 25, 16)),
            Shift(shift_id="2024, 4, 25,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 25, 16), end_time=datetime.datetime(2024, 4, 26, 0)),
            Shift(shift_id="2024, 4, 25,thursday_backup", shift_type=ShiftTypesEnum.THURSDAY_BACKUP, start_time=datetime.datetime(2024, 4, 25, 19, 30), end_time=datetime.datetime(2024, 4, 26, 2)),
            Shift(shift_id="2024, 4, 25,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 25, 21, 30), end_time=datetime.datetime(2024, 4, 26, 2))]
friday = [Shift(shift_id="2024, 4, 26,weekend_morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 4, 26, 7, 30), end_time=datetime.datetime(2024, 4, 26, 14, 30)),
          Shift(shift_id="2024, 4, 26,weekend_morning_backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 26, 8), end_time=datetime.datetime(2024, 4, 26, 17)),
          Shift(shift_id="2024, 4, 26,weekend_morning_backup2", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 26, 11, 30), end_time=datetime.datetime(2024, 4, 26, 19)),
          Shift(shift_id="2024, 4, 26,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 26, 16, 30), end_time=datetime.datetime(2024, 4, 27, 0)),
          Shift(shift_id="2024, 4, 26,weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 4, 26, 21, 30), end_time=datetime.datetime(2024, 4, 27, 2)),
          Shift(shift_id="2024, 4, 26,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 26, 22), end_time=datetime.datetime(2024, 4, 27, 2))]
saturday = [Shift(shift_id="2024, 4, 27,weekend_morning", shift_type=ShiftTypesEnum.WEEKEND_MORNING, start_time=datetime.datetime(2024, 4, 27, 7, 30), end_time=datetime.datetime(2024, 4, 27, 14, 30)),
            Shift(shift_id="2024, 4, 27,weekend_morning_backup", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 27, 8), end_time=datetime.datetime(2024, 4, 27, 17)),
            Shift(shift_id="2024, 4, 27,weekend_morning_backup2", shift_type=ShiftTypesEnum.WEEKEND_MORNING_BACKUP, start_time=datetime.datetime(2024, 4, 27, 11, 30), end_time=datetime.datetime(2024, 4, 27, 19)),
            Shift(shift_id="2024, 4, 27,evening", shift_type=ShiftTypesEnum.EVENING, start_time=datetime.datetime(2024, 4, 27, 16, 30), end_time=datetime.datetime(2024, 4, 28, 0)),
            Shift(shift_id="2024, 4, 27,weekend_evening_backup", shift_type=ShiftTypesEnum.WEEKEND_EVENING_BACKUP, start_time=datetime.datetime(2024, 4, 27, 21, 30), end_time=datetime.datetime(2024, 4, 28, 2)),
            Shift(shift_id="2024, 4, 27,closing", shift_type=ShiftTypesEnum.CLOSING, start_time=datetime.datetime(2024, 4, 27, 22), end_time=datetime.datetime(2024, 4, 28, 2))]

week_21_to_27_to_april = sunday + monday + tuesday + wednesday + thursday + friday + saturday
