from Outputs.EffortOutput import EffortOutput


class ResourceLackOutput:

    def __init__(self, business_line: str, system: str):
        self.business_line: str = business_line
        self.system: str = system
        self.efforts: [EffortOutput] = []