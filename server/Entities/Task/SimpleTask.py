from Entities.Assignment.AssignmentEntry import AssignmentEntry
from Entities.Assignment.Assignments import Assignments
from Entities.Resource.Resource import Resource
from copy import copy

from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Task.Effort.Efforts import Efforts
from datetime import date

from Entities.Team.Team import Team


class SimpleTask(Task):

    def __init__(self, id: str, name: str, business_line: str, efforts: Efforts, team: Team):
        self.id: str = id
        self.name: str = name
        self.business_line: str = business_line
        self.sub_tasks: [Task] = []
        self.initial_efforts: Efforts = copy(efforts)
        self.remaining_efforts: Efforts = efforts
        self.team: Team = team
        self.assignments: Assignments = Assignments()
        self.start_and_end_date_if_initial_effort_is_zero = None

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_business_line(self):
        return self.business_line

    def get_team(self):
        return self.team

    def can_be_worked_on_date(self, date: date):
        return True

    def get_direct_sub_tasks(self):
        return self.sub_tasks

    def set_direct_sub_tasks(self, sub_tasks: []):
        assert all([isinstance(sub_task, Task) for sub_task in sub_tasks])
        self.sub_tasks = sub_tasks

    def get_initial_efforts_hours_ignoring_sub_tasks(self):
        return self.initial_efforts.get_hours()

    def get_initial_efforts_hours_for_sub_tasks(self):
        return sum([sub_task.get_initial_efforts_hours() for sub_task in self.sub_tasks])

    def get_initial_efforts_hours_for_skill_ignoring_sub_tasks(self, skill: Skill):
        return self.initial_efforts.get_hours_for_skill(skill=skill)

    def get_initial_efforts_hours(self) -> float:
        self_hours = self.get_initial_efforts_hours_ignoring_sub_tasks()
        child_hours = self.get_initial_efforts_hours_for_sub_tasks()
        return self_hours + child_hours

    def get_initial_efforts_ignoring_sub_tasks(self):
        return self.initial_efforts

    def get_initial_efforts(self):
        result = self.initial_efforts
        for sub_task in self.sub_tasks:
            result = result + sub_task.get_initial_efforts()

        return result

    def get_remaining_efforts(self):
        result = self.remaining_efforts
        for sub_task in self.sub_tasks:
            result = result + sub_task.get_remaining_efforts()

        return result

    def get_remaining_efforts_ignoring_sub_tasks(self):
        return self.remaining_efforts

    def get_remaining_efforts_hours_ignoring_sub_tasks(self):
        return self.remaining_efforts.get_hours()

    def get_remaining_efforts_hours_for_sub_tasks(self):
        return sum([sub_task.get_remaining_efforts_hours() for sub_task in self.sub_tasks])

    def get_remaining_efforts_hours(self) -> float:
        self_hours = self.get_remaining_efforts_hours_ignoring_sub_tasks()
        child_hours = self.get_remaining_efforts_hours_for_sub_tasks()
        return self_hours + child_hours

    def get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(self, skill: Skill):
        return self.remaining_efforts.get_hours_for_skill(skill=skill)

    def get_remaining_efforts_hours_for_skill_for_sub_tasks(self, skill: Skill):
        return sum([sub_task.get_remaining_efforts_hours_for_skill(skill=skill) for sub_task in self.sub_tasks])

    def get_remaining_efforts_hours_for_skill(self, skill: Skill):
        self_hours = self.get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(skill=skill)
        child_hours = self.get_remaining_efforts_hours_for_skill_for_sub_tasks(skill=skill)
        return self_hours + child_hours

    def remove_assignments_by_resource_and_date_and_skill(self, resource: Resource, date: date, skill: Skill):
        assignments_to_keep = []
        assignments_to_remove = []

        for old_assignment in self.assignments.assignment_list:
            if old_assignment.resource == resource and old_assignment.date == date and old_assignment.skill == skill:
                assignments_to_remove.append(old_assignment)
            else:
                assignments_to_keep.append(old_assignment)

        for assignment_to_remove in assignments_to_remove:
            effort_hours_to_increase = -assignment_to_remove.task_effort_decrease_hours
            self.remaining_efforts.decrease_hours_for_skill(skill=skill, hours=effort_hours_to_increase)

        self.assignments.assignment_list = assignments_to_keep

    def accept_assignment(self, assignment: AssignmentEntry):
        skill = assignment.skill
        task_effort_decrease_hours = assignment.task_effort_decrease_hours
        self.remaining_efforts.decrease_hours_for_skill(skill=skill, hours=task_effort_decrease_hours)
        self.assignments.assignment_list.append(assignment)

    def get_assignments(self):
        return self.assignments

    def get_assignment_entries_for_resource(self, resource: Resource):
        return self.assignments.get_assignment_entries_for_task_and_resource(task=self, resource=resource)

    def has_start_date(self):
        if self.start_and_end_date_if_initial_effort_is_zero:
            return True

        must_have_its_own_start_date = self.get_initial_efforts_hours_ignoring_sub_tasks() > 0

        if must_have_its_own_start_date:
            return self.assignments.has_start_date() and all([sub_task.has_start_date() for sub_task in self.sub_tasks])
        else:
            has_start_date_for_subtasks = [sub_task.has_start_date() for sub_task in self.sub_tasks]
            have_at_least_one_subtask = len(has_start_date_for_subtasks) > 0
            return have_at_least_one_subtask and all(has_start_date_for_subtasks)

    def get_start_date(self):
        if self.start_and_end_date_if_initial_effort_is_zero:
            return self.start_and_end_date_if_initial_effort_is_zero

        if self.has_start_date():
            task_start_date_list = [self.assignments.get_start_date()] if self.assignments.has_start_date() else []
            sub_tasks_start_date_list = [sub_task.get_start_date() for sub_task in self.sub_tasks if sub_task.has_start_date()]

            start_dates = task_start_date_list + sub_tasks_start_date_list

            return min(start_dates)
        else:
            raise ValueError

    def has_end_date(self):
        if self.start_and_end_date_if_initial_effort_is_zero:
            return True

        must_have_its_own_end_date = self.get_initial_efforts_hours_ignoring_sub_tasks() > 0

        if must_have_its_own_end_date:
            return \
                self.get_remaining_efforts_hours_ignoring_sub_tasks() == 0 \
                and self.assignments.has_end_date() \
                and all([sub_task.has_end_date() for sub_task in self.sub_tasks])
        else:
            has_end_date_for_subtasks = [sub_task.has_end_date() for sub_task in self.sub_tasks]
            have_at_least_one_subtask = len(has_end_date_for_subtasks) > 0
            return have_at_least_one_subtask and all(has_end_date_for_subtasks)

    def get_end_date(self):
        if self.start_and_end_date_if_initial_effort_is_zero:
            return self.start_and_end_date_if_initial_effort_is_zero

        if self.has_end_date():
            task_end_date_list = [self.assignments.get_end_date()] if self.assignments.has_end_date() else []
            sub_tasks_end_date_list = [sub_task.get_end_date() for sub_task in self.sub_tasks if sub_task.has_end_date()]

            end_dates = task_end_date_list + sub_tasks_end_date_list

            return max(end_dates)
        else:
            raise ValueError

    def set_preferred_start_and_end_date_if_initial_effort_is_zero(self, preferred_start_and_end_date: date):
        if self.get_initial_efforts_hours() == 0:
            self.start_and_end_date_if_initial_effort_is_zero = preferred_start_and_end_date
        else:
            raise ValueError('SimpleTask set_preferred_start_and_end_date_if_initial_effort_is_zero initial start_and_end_date can be set only if initial effort is zero.')
