from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Team.GroupOfMembersHavingSameSkill import GroupOfMembersHavingSameSkill
import datetime

from Entities.Team.Member import Member


class Team:

    def __init__(self, business_line: str):
        self.business_line: str = business_line
        self.groups: [GroupOfMembersHavingSameSkill] = []
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
            group = GroupOfMembersHavingSameSkill(skill=member_skill)
            self.groups.append(group)
        else:
            group = self.get_group_for_skill(skill=member_skill)

        group.members.append(member)

    def put_picked_resources_to_the_end_of_available_resources_list(self, picked_resources: [Resource], available_resources: [Resource]) -> [Resource]:
        return [resource for resource in available_resources if resource not in picked_resources] + picked_resources

    def pick_resources_for_task(self, task: Task, start_date: datetime.date, end_date: datetime.date):
        available_resources = self.resource_pool
        for group in self.groups:
            group.pick_resources_for_task(task=task, start_date=start_date, end_date=end_date, resource_pool=available_resources)
            picked_resources = group.get_picked_resources()
            available_resources = self.put_picked_resources_to_the_end_of_available_resources_list(
                picked_resources=picked_resources,
                available_resources=available_resources
            )

    def get_members(self):
        result = []
        for group in self.groups:
            result = result + group.members

        return result
