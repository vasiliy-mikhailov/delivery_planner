from Inputs.CapacityInput import CapacityInput


class ExistingResourceInput:

    def __init__(self, id: str, name: str, business_line: str, calendar: str, hours_per_day: float):
        self.id: str = id
        self.name: str = name
        self.business_line: str = business_line
        self.calendar: str = calendar
        self.hours_per_day: float = hours_per_day
        self.capacity_per_day: [CapacityInput] = []
