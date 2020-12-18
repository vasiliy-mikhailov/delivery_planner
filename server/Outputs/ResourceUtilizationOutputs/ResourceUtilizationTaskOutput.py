class ResourceUtilizationTaskOutput:

    def __init__(self, id: str, name: str):
        self.id: str = id
        self.name: str = name
        self.hours_spent_by_day: {} = {}