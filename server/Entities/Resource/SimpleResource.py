from Entities.Assignment.AssignmentEntry import AssignmentEntry
from Entities.Assignment.Assignments import Assignments
from Entities.Resource.Capacity.Capacities import Capacities
import datetime
from Entities.Skill.Skill import Skill
from Entities.Task.Task import Task
from Entities.Resource.Calendar.Calendar import generate_date_range
from Entities.Resource.Resource import Resource

class SimpleResource(Resource):

    def __init__(self, id: str, name: str, work_date_start: datetime.date, work_date_end: datetime.date,
                 business_line: str, capacities: Capacities):
        self.id: str = id
        self.name: str = name
        self.work_date_start: datetime.date = work_date_start
        self.work_date_end: datetime.date = work_date_end
        self.initial_work_hours_for_date: {} = {}
        self.remaining_work_hours_for_date: {} = {}
        for day in generate_date_range(start_date=work_date_start, end_date=work_date_end):
            work_hours = capacities.get_work_hours_for_date(date=day)
            self.initial_work_hours_for_date[day] = work_hours
            self.remaining_work_hours_for_date[day] = work_hours
        self.business_line: str = business_line
        self.capacities: Capacities = capacities
        self.assignments: Assignments = Assignments()

    def get_remaining_work_hours(self):
        return sum(self.remaining_work_hours_for_date.values())

    def get_initial_work_hours(self):
        return sum(self.initial_work_hours_for_date.values())

    def has_start_date(self):
        return self.assignments.has_start_date()

    def get_start_date(self):
        return self.assignments.get_start_date()

    def has_end_date(self):
        return self.assignments.has_end_date()

    def get_end_date(self):
        return self.assignments.get_end_date()

    def get_remaining_work_hours_for_date(self, date: datetime.date):
        if date in self.remaining_work_hours_for_date:
            return self.remaining_work_hours_for_date[date]
        else:
            return 0

    def get_initial_work_hours_for_date(self, date: datetime.date):
        if date in self.initial_work_hours_for_date:
            return self.initial_work_hours_for_date[date]
        else:
            return 0

    def is_helpful_in_performing_task_for_date(self, task: Task, date: datetime.date) -> bool:
        remaining_work_hours_for_date = self.get_remaining_work_hours_for_date(date=date)
        return remaining_work_hours_for_date > 0 \
            and (self.business_line == task.get_business_line() or not self.business_line) \
            and self.capacities.is_helpful_in_performing_task(task=task)

    def is_helpful_in_performing_task_and_belongs_to_business_line_and_has_skill(self, task: Task, business_line: str, skill: Skill):
        remaining_work_hours = self.get_remaining_work_hours()

        return remaining_work_hours > 0 \
            and (self.business_line == business_line or self.business_line == '') \
            and self.capacities.is_helpful_in_performing_task_and_has_skill(
                task=task,
                skill=skill
            )

    def get_tasks(self):
        return self.assignments.get_tasks()

    def remove_assignments_by_task_and_date_and_skill(self, task: Task, date: datetime.date, skill: Skill):
        assignments_to_keep = []
        assignments_to_remove = []

        for old_assignment in self.assignments.assignment_list:
            if old_assignment.task == task and old_assignment.date == date and old_assignment.skill == skill:
                assignments_to_remove.append(old_assignment)
            else:
                assignments_to_keep.append(old_assignment)

        for assignment_to_remove in assignments_to_remove:
            work_hours_to_increase = assignment_to_remove.resource_spent_hours
            self.remaining_work_hours_for_date[date] = self.remaining_work_hours_for_date[date] + work_hours_to_increase

        self.assignments.assignment_list = assignments_to_keep

    def accept_assignment(self, assignment: AssignmentEntry):
        assignment_date = assignment.date
        resource_spent_hours = assignment.resource_spent_hours
        self.remaining_work_hours_for_date[assignment_date] = self.remaining_work_hours_for_date[
                                                                  assignment_date] - resource_spent_hours
        self.assignments.assignment_list.append(assignment)

    def get_task_effort_decrease_for_task_and_date_and_skill(
            self,
            task: Task,
            date: datetime.date,
            skill: Skill
    ):
        return sum([assignment.task_effort_decrease_hours for assignment in self.assignments.assignment_list if
                    assignment.task == task
                    and assignment.date == date
                    and assignment.skill == skill])

    def get_hours_spent_for_task_and_date_and_skill(
            self,
            task: Task,
            date: datetime.date,
            skill: Skill
    ):
        return sum([assignment.resource_spent_hours for assignment in self.assignments.assignment_list if
                    assignment.task == task
                    and assignment.date == date
                    and assignment.skill == skill])

    def get_efficiency_for_date_and_skill(
            self,
            date: datetime.date,
            skill: Skill
        ):
        return self.capacities.get_efficiency_for_date_and_skill(
            date=date,
            skill=skill
        )

    def get_assignment_entries_for_task_and_skill(
            self,
            task: Task,
            skill: Skill
        ):
        return self.assignments.get_assignment_entries_for_task_and_skill(task=task, resource=self, skill=skill)

    def has_skill(self, skill: Skill):
        return self.capacities.has_skill(skill=skill)