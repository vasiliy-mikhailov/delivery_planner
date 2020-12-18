from datetime import date

from Entities.Resource.EfficiencyInTime.EfficiencyInTime import EfficiencyInTime


class ConstantEfficiency(EfficiencyInTime):

    def get_resource_efficiency_for_date(self, date: date) -> float:
        return 1.0