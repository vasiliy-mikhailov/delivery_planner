from Entities.Skill.AbilityEnum import AbilityEnum


class ResourceCalendarPlanBottleneckHintOutput:

    def __init__(self, task_id: str, system: str, ability: AbilityEnum):
        self.task_id: str = task_id
        self.system: str = system
        self.ability: AbilityEnum = ability