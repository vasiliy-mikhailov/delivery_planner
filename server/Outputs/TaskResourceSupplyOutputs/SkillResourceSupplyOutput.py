from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.HightlightOutput import HighlightOutput


class SkillResourceSupplyOutput:

    def __init__(self, system: str, ability: AbilityEnum, supply_percent: float, highlight: HighlightOutput):
        self.system: str = system
        self.ability: AbilityEnum = ability
        self.supply_percent: float = supply_percent
        self.highlight: HighlightOutput = highlight
