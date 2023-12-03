from datetime import time
from enum import Enum


# Need to think of a better solution for the shifts start time and end time storing or receiving form.
class ShiftTimes(Enum):
    morning_shift_times = {"start": time(11, 45), "end": time(17, 0)}
    evening_shift_times = {"start": time(17, 0), "end": time(22, 0)}
    thu_evening_shift_times = {"start": time(16, 0), "end": time(22, 0)}
    thu_backup_shift_times = {"start": time(19, 30), "end": time(0, 0)}
    thu_closing_shift_times = {"start": time(21, 30), "end": time(2, 0)}
    closing_shift_times = {"start": time(19, 30), "end": time(2, 0)}
    weekend_morning_shift_time = {"start": time(9, 15), "end": time(18, 0)}
    weekend_backup_shift_times = {"start": time(12, 0), "end": time(18, 0)}
    weekend_evening_shift_times = {"start": time(18, 0), "end": time(22, 0)}
    weekend_closing_shift_times = {"start": time(21, 30), "end": time(2, 0)}
