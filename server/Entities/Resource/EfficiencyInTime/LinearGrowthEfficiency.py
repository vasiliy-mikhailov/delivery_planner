import datetime

from Entities.Resource.EfficiencyInTime.EfficiencyInTime import EfficiencyInTime


class LinearGrowthEfficiency(EfficiencyInTime):

    def __init__(self, start_date: datetime.date, full_efficiency_date: datetime.date):
        self.start_date: datetime.date = start_date
        self.full_efficiency_date: datetime.date = full_efficiency_date

    def get_resource_efficiency_for_date(self, date: datetime.date) -> float:
        if self.start_date > self.full_efficiency_date:
            return 1.0

        if date < self.start_date:
            return 0.0
        elif date > self.full_efficiency_date:
            return 1.0
        else:
            days_passed_from_start = (date - self.start_date).days + 1
            days_between_start_and_full_efficiency = (self.full_efficiency_date - self.start_date).days + 1
            return float(days_passed_from_start) / float(days_between_start_and_full_efficiency)
