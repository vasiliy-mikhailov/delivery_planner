from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Team.Group import Group
import datetime

from Entities.Team.Member import Member


class Team:

    def __init__(self, business_line: str):
        self.business_line: str = business_line
        self.groups: [Group] = []
        self.resource_pool: [Resource] = []

    def has_group_for_skill(self, skill: Skill):
        return any([group for group in self.groups if group.skill == skill])

    def get_group_for_skill(self, skill: Skill):
        groups_with_skill = [group for group in self.groups if group.skill == skill]

        if len(groups_with_skill) == 1:
            return groups_with_skill[0]
        else:
            raise ValueError

    def add_member(self, member: Member):
        member_skill = member.get_skill()
        if not self.has_group_for_skill(skill=member_skill):
            group = Group(skill=member_skill)
            self.groups.append(group)
        else:
            group = self.get_group_for_skill(skill=member_skill)

        group.members.append(member)

    def pick_resources_for_task(self, task: Task, start_date: datetime.date, end_date: datetime.date):
        resources_left = self.resource_pool
        for group in self.groups:
            group.pick_resources_for_task(task=task, start_date=start_date, end_date=end_date, resource_pool=resources_left)
            picked_resources = group.get_picked_resources()
            resources_left = [resource for resource in resources_left if resource not in picked_resources]


    def get_members(self):
        result = []
        for group in self.groups:
            result = result + group.members

        return result





