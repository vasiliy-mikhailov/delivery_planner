from Entities.ExternalTask.ExternalTask import ExternalTask


class ExternalTaskRepository:

    def get_external_task_by_id(self, external_task_id: str) -> ExternalTask:
        raise NotImplementedError

    def has_external_task_with_id(self, external_task_id: str) -> bool:
        raise NotImplementedError