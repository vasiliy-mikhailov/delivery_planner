from Entities.ExternalTask.ExternalTaskEffort import ExternalTaskEffort


class ExternalTask:

    def __init__(self, id: str, name: str, system: str):
        self.id: str = id
        self.name: str = name
        self.system: str = system
        self.efforts: [ExternalTaskEffort] = []
        self.sub_tasks: [ExternalTask] = []

    def efforts_equal(self, efforts, other_efforts) -> bool:
        if len(efforts) != len(other_efforts):
            return False

        for effort in efforts:
            if effort not in other_efforts:
                return False

        return True

    def sub_tasks_equal(self, sub_tasks, other_sub_tasks) -> bool:
        if len(sub_tasks) != len(other_sub_tasks):
            return False

        for sub_task in sub_tasks:
            if sub_task not in other_sub_tasks:
                return False

        return True

    def __eq__(self, other):
        return \
            self.id == other.id \
            and self.name == other.name \
            and self.system == other.system \
            and self.efforts_equal(efforts=self.efforts, other_efforts=other.efforts) \
            and self.sub_tasks_equal(sub_tasks=self.sub_tasks, other_sub_tasks=other.sub_tasks)
