import datetime

from Entities.Resource.EfficiencyInTime.EfficiencyInTime import EfficiencyInTime


class TimeBoundedConstantEfficiency(EfficiencyInTime):
    def __init__(self, start_date: datetime.date, end_date: datetime.date):
        self.start_date: datetime.date = start_date
        self.end_date: datetime.date = end_date

    def get_resource_efficiency_for_date(self, date: datetime.date) -> float:
        date_is_between_start_date_and_end_date = date >= self.start_date and date <= self.end_date
        if date_is_between_start_date_and_end_date:
            return 1.0
        else:
            return 0.0