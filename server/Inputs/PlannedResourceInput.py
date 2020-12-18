from datetime import date
from Inputs.CapacityInput import CapacityInput


class PlannedResourceInput:

    def __init__(self, id: str, name: str, business_line: str, start_date: date, full_power_in_month: float, calendar: str, hours_per_day: float):
        self.id: str = id
        self.name: str = name
        self.business_line: str = business_line
        self.start_date: date = start_date
        self.full_power_in_month: float = full_power_in_month
        self.calendar: str = calendar
        self.hours_per_day: float = hours_per_day
        self.capacity_per_day: [CapacityInput] = []
