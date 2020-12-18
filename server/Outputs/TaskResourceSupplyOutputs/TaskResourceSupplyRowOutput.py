from Outputs.HightlightOutput import HighlightOutput
from Outputs.TaskResourceSupplyOutputs.SkillResourceSupplyOutput import SkillResourceSupplyOutput

class TaskResourceSupplyRowOutput:

    def __init__(self, task_id: str, task_name: str, business_line: str, is_fully_supplied: bool, is_fully_supplied_highlight: bool):
        self.task_id: str = task_id
        self.task_name: str = task_name
        self.business_line: str = business_line
        self.is_fully_supplied: bool = is_fully_supplied
        self.is_fully_supplied_highlight: HighlightOutput = is_fully_supplied_highlight
        self.skill_resource_supply: [SkillResourceSupplyOutput] = []

