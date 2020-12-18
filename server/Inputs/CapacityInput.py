import math

from Entities.Skill.AbilityEnum import AbilityEnum


class CapacityInput:

    def __init__(self, system: str, ability: AbilityEnum, efficiency: float):
        if not isinstance(system, str):
            raise ValueError('CapacityInput __init__ parameter "system" must be str.')

        if isinstance(efficiency, float) and math.isnan(efficiency):
            raise ValueError('CapacityInput __init__ parameter "efficiency" cannot be nan.')

        self.system: str = system
        self.ability: AbilityEnum = ability
        self.efficiency: float = efficiency
