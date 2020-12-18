from datetime import datetime
from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Team.Member import Member


class Group:

    def __init__(self, skill: Skill):
        self.skill: Skill = skill
        self.members: [Member] = []
        self.is_bottleneck: bool = False

    def pick_resources_for_task(self, task: Task, start_date: datetime.date, end_date: datetime.date, resource_pool: [Resource]):
        resources_left = resource_pool
        for member in self.members:
            member.pick_resource_for_task(task=task, start_date=start_date, end_date=end_date, resource_pool=resources_left)
            if member.has_picked_resource():
                picked_resource = member.get_picked_resource()
                resources_left = [resource for resource in resources_left if resource != picked_resource]

    def get_picked_resources(self):
        result = []

        for member in self.members:
            if member.has_picked_resource():
                result.append(member.get_picked_resource())

        return result

    def has_assignment_end_date_for_task(self, task: Task):
        for member in self.members:
            has_picked_resource = member.has_picked_resource()
            if not has_picked_resource:
                return False

            picked_resource = member.get_picked_resource()

            assignment_entries = task.get_assignment_entries_for_resource(resource=picked_resource)

            if not assignment_entries:
                return False

        return True

    def get_assignment_end_date_for_task(self, task: Task) -> datetime.date:
        result = None

        for member in self.members:
            has_picked_resource = member.has_picked_resource()
            if not has_picked_resource:
                raise ValueError

            picked_resource = member.get_picked_resource()

            assignment_entries = task.get_assignment_entries_for_resource(resource=picked_resource)

            if not assignment_entries:
                raise ValueError

            latest_assignment = max([assignment.date for assignment in assignment_entries])

            if not result or result < latest_assignment:
                result = latest_assignment

        return latest_assignment
