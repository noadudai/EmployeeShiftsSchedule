import datetime
from dataclasses import dataclass


@dataclass
class DayOffPreference:
    day_date: datetime.date
