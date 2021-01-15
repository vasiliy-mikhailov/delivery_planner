from datetime import date

from Entities.Resource.Resource import Resource
from Entities.Skill.Skill import Skill


class Task:

    def can_be_worked_on_date(self, date: date):
        raise NotImplementedError

    def get_assignment_entries_for_resource(self, resource: Resource):
        raise NotImplementedError

    def get_id(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_business_line(self):
        raise NotImplementedError

    def get_team(self):
        raise NotImplementedError

    def get_direct_sub_tasks(self):
        raise NotImplementedError

    def get_initial_efforts_hours(self) -> float:
        raise NotImplementedError

    def get_initial_efforts(self):
        raise NotImplementedError

    def get_initial_efforts_ignoring_sub_tasks(self):
        raise NotImplementedError

    def get_initial_efforts_hours_for_skill_ignoring_sub_tasks(self, skill: Skill):
        raise NotImplementedError

    def get_assignments(self):
        raise NotImplementedError

    def set_direct_sub_tasks(self, sub_tasks: []):
        raise NotImplementedError

    def get_remaining_efforts(self):
        raise NotImplementedError

    def get_remaining_efforts_hours_for_skill(self, skill: Skill):
        raise NotImplementedError

    def get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(self, skill: Skill):
        raise NotImplementedError

    def accept_assignment(self, assignment):
        raise NotImplementedError

    def get_remaining_efforts_hours(self) -> float:
        raise NotImplementedError

    def has_start_date(self):
        raise NotImplementedError

    def get_start_date(self):
        raise NotImplementedError

    def has_end_date(self):
        raise NotImplementedError

    def get_end_date(self):
        raise NotImplementedError

    def remove_assignments_by_resource_and_date_and_skill(self, resource: Resource, date: date, skill: Skill):
        raise NotImplementedError

    def set_preferred_start_and_end_date_if_initial_effort_is_zero(self, preferred_start_and_end_date: date):
        raise NotImplementedError