from datetime import date
from Inputs.CapacityInput import CapacityInput


class TemporaryResourceInput:

    def __init__(self, id: str, name: str, business_line: str, has_start_date: bool, start_date: date, has_end_date: bool, end_date: date, calendar: str, hours_per_day: float):
        self.id: str = id
        self.name: str = name
        self.business_line: str = business_line
        self.has_start_date: bool = has_start_date
        self.start_date: date = start_date
        self.has_end_date: bool = has_end_date
        self.end_date: date = end_date
        self.calendar: str = calendar
        self.hours_per_day: float = hours_per_day
        self.capacity_per_day: [CapacityInput] = []
