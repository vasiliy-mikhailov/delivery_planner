from Entities.Assignment.AssignmentEntry import AssignmentEntry
from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from datetime import date


class FinishStartConstrainedTask(Task):

    def __init__(self, task: Task):
        self.task: Task = task
        self.predecessors: [Task] = []
        self.start_and_end_date_if_initial_effort_is_zero: date = None

    def get_assignment_entries_for_resource(self, resource: Resource):
        return self.task.get_assignment_entries_for_resource(resource=resource)

    def get_id(self):
        return self.task.get_id()

    def are_all_predecessors_have_end_date(self):
        return all([predecessor.has_end_date() for predecessor in self.predecessors])

    def get_predecessors_max_end_date(self):
        return max([predecessor.get_end_date() for predecessor in self.predecessors])

    def can_be_worked_on_date(self, date: date):
        return self.are_all_predecessors_have_end_date() and date > self.get_predecessors_max_end_date()

    def get_business_line(self):
        return self.task.get_business_line()

    def get_remaining_efforts(self):
        return self.task.get_remaining_efforts()

    def get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(self, skill: Skill):
        return self.task.get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(skill=skill)

    def accept_assignment(self, assignment: AssignmentEntry):
        assignment_date = assignment.date
        if self.can_be_worked_on_date(date=assignment_date):
            return self.task.accept_assignment(assignment=assignment)
        else:
            raise ValueError

    def get_assignments(self):
        return self.task.get_assignments()

    def get_direct_sub_tasks(self):
        return self.task.get_direct_sub_tasks()

    def get_name(self):
        return self.task.get_name()

    def get_team(self):
        return self.task.get_team()

    def set_direct_sub_tasks(self, sub_tasks: []):
        self.task.set_direct_sub_tasks(sub_tasks=sub_tasks)

    def get_remaining_efforts_hours(self) -> float:
        return self.task.get_remaining_efforts_hours()

    def get_remaining_efforts_hours_for_skill(self, skill: Skill):
        return self.task.get_remaining_efforts_hours_for_skill(skill=skill)

    def has_start_date(self):
        initial_effort_hours = self.get_initial_efforts_hours()

        if initial_effort_hours == 0:
            return self.are_all_predecessors_have_end_date()
        else:
            return self.task.has_start_date()

    def get_start_date(self):
        initial_effort_hours = self.get_initial_efforts_hours()

        if initial_effort_hours == 0:
            return self.get_predecessors_max_end_date()
        else:
            return self.task.get_start_date()

    def has_end_date(self):
        initial_effort_hours = self.get_initial_efforts_hours()

        if initial_effort_hours == 0:
            return self.are_all_predecessors_have_end_date()
        else:
            return self.task.has_end_date()

    def get_end_date(self):
        initial_effort_hours = self.get_initial_efforts_hours()

        if initial_effort_hours == 0:
            return self.get_predecessors_max_end_date()
        else:
            return self.task.get_end_date()

    def intentionally_do_nothing(self):
        pass

    def set_preferred_start_and_end_date_if_initial_effort_is_zero(self, preferred_start_and_end_date: date):
        initial_effort_hours = self.get_initial_efforts_hours()

        if initial_effort_hours == 0:
            self.intentionally_do_nothing()
        else:
            raise ValueError('FinishStartConstrainedTask set_preferred_start_and_end_date_if_initial_effort_is_zero initial start_and_end_date can be set only if initial effort is zero.')


    def get_initial_efforts_hours(self) -> float:
        return self.task.get_initial_efforts_hours()

    def get_initial_efforts(self):
        return self.task.get_initial_efforts()

    def get_initial_efforts_ignoring_sub_tasks(self):
        return self.task.get_initial_efforts_ignoring_sub_tasks()

    def get_initial_efforts_hours_for_skill_ignoring_sub_tasks(self, skill: Skill):
        return self.task.get_initial_efforts_hours_for_skill_ignoring_sub_tasks(skill=skill)

    def remove_assignments_by_resource_and_date_and_skill(self, resource: Resource, date: date, skill: Skill):
        self.task.remove_assignments_by_resource_and_date_and_skill(resource=resource, date=date, skill=skill)