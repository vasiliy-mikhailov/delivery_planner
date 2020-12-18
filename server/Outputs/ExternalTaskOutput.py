from Outputs.EffortOutput import EffortOutput


class ExternalTaskOutput:

    def __init__(self, id: str, name: str, system: str, business_line: str):
        self.id: str = id
        self.name: str = name
        self.system: str = system
        self.business_line: str = business_line
        self.efforts: [EffortOutput] = []
        self.sub_tasks: [ExternalTaskOutput] = []