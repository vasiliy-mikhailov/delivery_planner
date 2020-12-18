from datetime import datetime
from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task


class Member:
    def pick_resource_for_task(self, task: Task, start_date: datetime.date, end_date: datetime.date, resource_pool: [Resource]):
        raise NotImplementedError

    def has_picked_resource(self):
        raise NotImplementedError

    def get_picked_resource(self):
        raise NotImplementedError

    def get_skill(self):
        raise NotImplementedError

    def set_skill(self, skill: Skill):
        raise NotImplementedError