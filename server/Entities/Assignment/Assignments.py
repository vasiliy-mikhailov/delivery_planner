from Entities.Assignment.AssignmentEntry import AssignmentEntry
from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task


class Assignments:

    def __init__(self):
        self.assignment_list: [] = []

    def has_start_date(self):
        return len(self.assignment_list) > 0

    def get_start_date(self):
        return min([assignment.date for assignment in self.assignment_list])

    def has_end_date(self):
        return len(self.assignment_list) > 0

    def get_end_date(self):
        return max([assignment.date for assignment in self.assignment_list])

    def get_resources(self):
        resources_with_repetition = [assignment_entry.resource for assignment_entry in self.assignment_list]

        distinct_resources = []

        for resource in resources_with_repetition:
            if not resource in distinct_resources:
                distinct_resources.append(resource)

        return distinct_resources

    def get_assignment_entries_for_task_and_resource(self, task: Task, resource: Resource) -> [AssignmentEntry]:
        result = [assignment_entry for assignment_entry in self.assignment_list if assignment_entry.task == task and assignment_entry.resource == resource]

        return result

    def get_assignment_entries_for_task_and_skill(
        self,
        task: Task,
        resource: Resource,
        skill: Skill
    ):
        result = [assignment_entry for assignment_entry in self.assignment_list if
                  assignment_entry.task == task
                  and assignment_entry.resource == resource
                  and assignment_entry.skill == skill
                  ]

        return result

    def get_tasks(self):
        tasks_with_repetition = [assignment_entry.task for assignment_entry in self.assignment_list]

        distinct_tasks = []

        for task in tasks_with_repetition:
            if not task in distinct_tasks:
                distinct_tasks.append(task)

        return distinct_tasks



