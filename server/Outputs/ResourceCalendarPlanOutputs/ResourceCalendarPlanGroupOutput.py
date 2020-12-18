from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.HightlightOutput import HighlightOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanMemberOutput import \
    ResourceCalendarPlanMemberOutput


class ResourceCalendarPlanGroupOutput:

    def __init__(
            self,
            system: str,
            ability: AbilityEnum,
            initial_hours: float,
            planned_hours: float,
            planned_readiness: float,
            highlight: HighlightOutput,
            is_bottleneck: bool
    ):
        self.system: str = system
        self.ability: AbilityEnum = ability
        self.initial_hours: float = initial_hours
        self.planned_hours: float = planned_hours
        self.planned_readiness: float = planned_readiness
        self.highlight: HighlightOutput = highlight
        self.is_bottleneck: bool = is_bottleneck
        self.members: ResourceCalendarPlanMemberOutput = []