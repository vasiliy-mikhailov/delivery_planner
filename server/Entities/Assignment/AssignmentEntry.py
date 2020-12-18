import math
from Entities.Resource.Resource import Resource
from Entities.Skill.AbilityEnum import AbilityEnum
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from datetime import date


def quantize_resource_spent_hours(resource_spent_hours: float) -> float:
    return AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS * math.floor(
        1 / AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS * resource_spent_hours)

class AssignmentEntry:

    MINIMAL_SPENDABLE_RESOURCE_HOURS = 0.5

    def __init__(
            self,
            task: Task,
            resource: Resource,
            date: date,
            skill: Skill,
            task_effort_decrease_hours: float,
            resource_spent_hours: float):

        if resource_spent_hours < AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS:
            raise ValueError(
                'AssignmentEntry __init__ parameter "resource_spent_hours" is {} which is too small. It must be greater or equal {}.'.format(
                    resource_spent_hours,
                    AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS
                )
            )

        if resource_spent_hours % AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS != 0:
            raise ValueError(
                'AssignmentEntry __init__ parameter "resource_spent_hours" is {} which is not which is not divisible by {} without remainder.'.format(
                    resource_spent_hours,
                    AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS
                )
            )

        self.task: Task = task
        self.resource: Resource = resource
        self.date: date = date
        self.skill: Skill = skill
        self.task_effort_decrease_hours: float = task_effort_decrease_hours
        self.resource_spent_hours: float = resource_spent_hours

