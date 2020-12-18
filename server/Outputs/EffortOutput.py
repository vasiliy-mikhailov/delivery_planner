import math

from Entities.Skill.AbilityEnum import AbilityEnum


class EffortOutput:

    def __init__(self, ability: AbilityEnum, hours: float):
        if not isinstance(ability, AbilityEnum):
            raise ValueError('EffortInput __init__ parameter "ability" must be AbilityEnum.')

        if isinstance(hours, float) and math.isnan(hours):
            raise ValueError('EffortInput __init__ parameter "hours" cannot be nan.')

        if hours == 0:
            raise ValueError('EffortInput __init__ parameter "hours" cannot be 0.')

        self.ability: AbilityEnum = ability
        self.hours: float = hours
