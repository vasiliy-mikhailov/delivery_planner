from Outputs.ResourceUtilizationOutputs.ResourceUtilizationTaskOutput import ResourceUtilizationTaskOutput


class ResourceUtilizationResourceOutput:

    def __init__(self, id: str, name: str, business_line: str):
        self.id: str = id
        self.name: str = name
        self.business_line: str = business_line
        self.utilization_by_date: {} = {}
        self.tasks: [ResourceUtilizationTaskOutput] = []
