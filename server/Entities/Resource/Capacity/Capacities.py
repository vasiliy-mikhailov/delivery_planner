from Entities.Resource.Calendar.Calendar import Calendar
from Entities.Resource.Capacity.CapacityEntry import CapacityEntry
from Entities.Resource.EfficiencyInTime.EfficiencyInTime import EfficiencyInTime
from datetime import date
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task


class Capacities:

    def __init__(self, work_hours_per_day: float, calendar: Calendar, efficiency_in_time: EfficiencyInTime):
        self.work_hours_per_day: float = work_hours_per_day
        self.calendar: Calendar = calendar
        self.efficiency_in_time: EfficiencyInTime = efficiency_in_time
        self.capacity_list = []

    def get_work_hours_for_date(self, date: date):
        if self.calendar.is_working_day(day=date):
            return self.work_hours_per_day
        else:
            return 0

    def is_helpful_in_performing_task(self, task: Task):
        return any([capacity_entry.is_helpful_in_performing_task(task=task) for capacity_entry in self.capacity_list])

    def is_helpful_in_performing_task_and_has_skill(self, task: Task, skill: Skill):
        return any([capacity_entry.is_helpful_in_performing_task(task=task) for capacity_entry in self.capacity_list if capacity_entry.skill == skill])

    def get_efficiency_for_date_and_skill(self, date: date, skill: Skill):
        efficiencies = [capacity.efficiency for capacity in self.capacity_list if capacity.skill == skill]

        if len(efficiencies) == 1:
            efficiency = efficiencies[0]
            return efficiency * self.efficiency_in_time.get_resource_efficiency_for_date(date=date)
        else:
            raise ValueError

    def has_skill(self, skill: Skill):
        return any([capacity for capacity in self.capacity_list if capacity.skill == skill])

    def get_capacity_for_skill(self, skill: Skill) -> CapacityEntry:
        capacity_list = [capacity for capacity in self.capacity_list if capacity.skill == skill]

        if len(capacity_list) == 1:
            return capacity_list[0]
        else:
            raise ValueError

