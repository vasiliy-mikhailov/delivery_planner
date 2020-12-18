from Entities.Skill.Skill import Skill
from Entities.Task.Effort.Effort import Effort
from copy import copy


class Efforts:

    def __init__(self, effort_entries: [Effort]):
        self.effort_entries = effort_entries

    def get_hours(self):
        return sum([x.hours for x in self.effort_entries])

    def get_hours_for_skill(self, skill: Skill):
        return sum([x.hours for x in self.effort_entries if x.skill == skill])

    def sum_efforts_by_skill_into_hashtable(self, effort_entries: [Effort]):
        result = {}

        for remaining_effort in effort_entries:
            skill = remaining_effort.skill
            if skill not in result:
                result[skill] = remaining_effort.hours
            else:
                result[skill] = result[skill] + remaining_effort.hours

        return result

    def convert_skill_to_hours_hashtable_into_task_effort_entity(self, skill_to_hours_hashtable: []):
        effort_entries: [Effort] = []

        for skill, hours in skill_to_hours_hashtable.items():
            effort = Effort(skill=skill, hours=hours)
            effort_entries.append(effort)

        result = Efforts(effort_entries=effort_entries)

        return result

    def __add__(self, other):
        skill_efforts_1 = self.effort_entries
        skill_efforts_2 = other.effort_entries
        all_efforts = skill_efforts_1 + skill_efforts_2
        skill_to_hours_hashtable = self.sum_efforts_by_skill_into_hashtable(
            effort_entries=all_efforts)
        result = self.convert_skill_to_hours_hashtable_into_task_effort_entity(skill_to_hours_hashtable=skill_to_hours_hashtable)

        return result

    def __copy__(self):
        return Efforts(effort_entries=[copy(e) for e in self.effort_entries])

    def decrease_hours_for_skill(self, skill: Skill, hours: float):
        for e in self.effort_entries:
            if e.skill == skill:
                e.hours = e.hours - hours
                break

    def get_skills(self):
        result = []

        for effort in self.effort_entries:
            skill = effort.skill

            if skill not in result:
                result.append(skill)

        return result