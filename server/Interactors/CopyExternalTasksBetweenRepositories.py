from Repository.ExternalTaskRepository.ExternalTaskRepository import ExternalTaskRepository


class CopyExternalTasksBetweenRepositories:

    def __init__(self, source_repository: ExternalTaskRepository, destination_repository: ExternalTaskRepository):
        self.source_repository: ExternalTaskRepository = source_repository
        self.destination_repository: ExternalTaskRepository = destination_repository

    def interact(self):
        source_repository = self.source_repository
        destination_repository = self.destination_repository
        external_tasks = source_repository.get_all()
        for external_task in external_tasks:
            destination_repository.save(external_task=external_task)
