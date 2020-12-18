import datetime

class VacationInput:

    def __init__(self, resource_id: str, start_date: datetime.date, end_date: datetime.date):
        self.resource_id: str = resource_id
        self.start_date: datetime.date = start_date
        self.end_date: datetime.date = end_date