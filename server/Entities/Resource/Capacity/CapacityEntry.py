from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task

class CapacityEntry:

    def __init__(self, skill: Skill, efficiency: float):
        self.skill = skill
        self.efficiency: float = efficiency

    def is_helpful_in_performing_task_ignoring_children(self, task: Task) -> bool:
        return task.get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(skill=self.skill) > 0

    def is_helpful_in_performing_task(self, task: Task) -> bool:
        if self.is_helpful_in_performing_task_ignoring_children(task=task):
            return True

        for sub_task in task.get_direct_sub_tasks():
            if self.is_helpful_in_performing_task(task=sub_task):
                return True

        return False