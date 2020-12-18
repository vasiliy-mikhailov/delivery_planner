from Entities.RepositoryTask.ExternalTask import ExternalTask

class ExternalTasks:

    def __init__(self):
        self.tasks: [ExternalTask] = []

    def get_tasks(self) -> [ExternalTask]:
        return self.tasks


