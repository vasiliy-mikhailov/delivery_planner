from Entities.RepositoryTask.ExternalTask import ExternalTask
from Entities.RepositoryTask.ExternalTaskEffort import ExternalTaskEffort
from Outputs.EffortOutput import EffortOutput
from Outputs.ExternalTaskOutput import ExternalTaskOutput


class ExternalTasksToExternalTaskOutputsConverter:

    def __init__(self, external_tasks: [ExternalTask]):
       self.external_tasks: [ExternalTask] = external_tasks

    def convert_external_task_effort_to_effort_output(self, external_task_effort: ExternalTaskEffort) -> EffortOutput:
        return EffortOutput(
            ability=external_task_effort.ability,
            hours=external_task_effort.hours
        )

    def convert_external_task_to_external_task_output(self, external_task: ExternalTask) -> ExternalTaskOutput:
        external_task_id = external_task.id
        external_task_name = external_task.name
        external_task_system = external_task.system
        external_task_business_line = external_task.business_line
        result = ExternalTaskOutput(
            id=external_task_id,
            name=external_task_name,
            system=external_task_system,
            business_line=external_task_business_line
        )

        result.efforts = [self.convert_external_task_effort_to_effort_output(external_task_effort=effort) for effort in external_task.efforts]

        result.sub_tasks = self.convert_external_tasks_to_external_task_outputs(external_tasks=external_task.sub_tasks)

        return result

    def convert_external_tasks_to_external_task_outputs(self, external_tasks: [ExternalTask]) -> [ExternalTaskOutput]:
        return [self.convert_external_task_to_external_task_output(external_task=external_task) for external_task in external_tasks]

    def convert(self):
        return self.convert_external_tasks_to_external_task_outputs(external_tasks=self.external_tasks)