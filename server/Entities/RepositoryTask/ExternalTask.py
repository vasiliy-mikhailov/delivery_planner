from Entities.RepositoryTask.ExternalTaskEffort import ExternalTaskEffort


class ExternalTask:

    def __init__(self, id: str, name: str, system: str, business_line: str, efforts: [ExternalTaskEffort]):
        self.id: str = id
        self.name: str = name
        self.system: str = system
        self.business_line: str = business_line
        self.efforts: [ExternalTaskEffort] = efforts
        self.sub_tasks: [ExternalTask] = []
