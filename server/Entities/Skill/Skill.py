from Entities.Skill.AbilityEnum import AbilityEnum


class Skill:
    def __init__(self, system: str, ability: AbilityEnum):
        self.system: str = system
        self.ability: AbilityEnum = ability

    def __eq__(self, other):
        return self.system == other.system and self.ability == other.ability

    def __hash__(self):
        return hash((self.system, self.ability))