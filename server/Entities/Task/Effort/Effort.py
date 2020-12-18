from Entities.Skill.Skill import Skill


class Effort:

    def __init__(self, skill: Skill, hours: float):
        self.skill: Skill = skill
        self.hours: float = hours
