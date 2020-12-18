from datetime import datetime
from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Team.Member import Member


class ConcreteResourceMember(Member):
    def __init__(self, skill: Skill, concrete_resource: Resource):
        concrete_resource_has_skill = concrete_resource.has_skill(skill)

        if not concrete_resource_has_skill:
            raise ValueError("ConcreteResourceMember __init__ resource concrete_resource {} does not have skill sys '{}' ability '{}'".format(
                concrete_resource.id,
                skill.system,
                skill.ability
            ))

        self.skill = skill
        self.concrete_resource = concrete_resource

    def get_skill(self):
        return self.skill

    def set_skill(self, skill: Skill):
        self.skill = skill

    def pick_resource_for_task(self, task: Task, start_date: datetime.date, end_date: datetime.date, resource_pool: [Resource]):
        pass

    def has_picked_resource(self):
        return True

    def get_picked_resource(self) -> [Resource]:
        return self.concrete_resource