from Entities.Skill.AbilityEnum import AbilityEnum


class ExternalTaskEffort:
    def __init__(self, ability: AbilityEnum, hours: float):
        self.ability: AbilityEnum = ability
        self.hours: float = hours

    def __eq__(self, other):
        return self.ability == other.ability and self.hours == other.hours