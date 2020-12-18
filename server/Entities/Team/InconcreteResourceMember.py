from datetime import datetime

from Entities.Resource.Calendar.Calendar import generate_date_range
from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Team.Member import Member


class InconcreteResourceMember(Member):
    def __init__(self, business_line: str, skill: Skill):
        self.business_line: str = business_line
        self.skill: Skill = skill
        self.picked_resource: Resource = None

    def get_skill(self):
        return self.skill

    def set_skill(self, skill: Skill):
        self.skill = skill

    def pick_resource_having_as_early_free_time_as_possible(self, resources: [Resource], start_date: datetime.date, end_date: datetime.date):
        for date in generate_date_range(start_date=start_date, end_date=end_date):
            for resource in resources:
                if resource.get_remaining_work_hours_for_date(date=date):
                    return resource

        raise ValueError('Cannot find free resource.')

    def pick_resource_for_task(self, task: Task, start_date: datetime.date, end_date: datetime.date, resource_pool: [Resource]):
        resources_conforming_to_requirements_and_helpful_in_solving_task = []

        skill = self.get_skill()

        for resource in resource_pool:
            if resource.is_helpful_in_performing_task_and_belongs_to_business_line_and_has_skill(
                task=task,
                business_line=self.business_line,
                skill=skill
            ):
                resources_conforming_to_requirements_and_helpful_in_solving_task.append(resource)

        try:
            earliest_available_resource = self.pick_resource_having_as_early_free_time_as_possible(
                resources=resources_conforming_to_requirements_and_helpful_in_solving_task,
                start_date=start_date,
                end_date=end_date
            )

            self.picked_resource = earliest_available_resource
        except (ValueError):
            pass

    def has_picked_resource(self):
        return self.picked_resource is not None

    def get_picked_resource(self) -> [Resource]:
        if self.has_picked_resource():
            return self.picked_resource
        else:
            raise ValueError

