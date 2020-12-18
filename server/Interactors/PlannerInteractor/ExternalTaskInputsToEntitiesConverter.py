from Entities.RepositoryTask.ExternalTask import ExternalTask
from Entities.RepositoryTask.ExternalTaskEffort import ExternalTaskEffort
from Inputs.EffortInput import EffortInput
from Inputs.ExternalTaskInput import ExternalTaskInput


class ExternalTaskInputsToEntitiesConverter:

    def __init__(self, external_task_inputs: [ExternalTaskInput]):
        self.external_task_inputs: [ExternalTaskInput] = external_task_inputs

    def convert_effort_input_to_external_task_effort(self, effort_input: EffortInput) -> ExternalTaskEffort:
        ability = effort_input.ability
        hours = effort_input.hours
        return ExternalTaskEffort(ability=ability, hours=hours)

    def convert_external_task_input_to_external_task(self, external_task_input: ExternalTaskInput) -> ExternalTask:
        task_id = external_task_input.id
        task_name = external_task_input.name
        task_system = external_task_input.system
        task_business_line = external_task_input.business_line
        external_task_efforts = [self.convert_effort_input_to_external_task_effort(effort_input=effort_input) for effort_input in external_task_input.efforts]

        result = ExternalTask(
            id=task_id,
            name=task_name,
            system=task_system,
            business_line=task_business_line,
            efforts=external_task_efforts
        )

        result.sub_tasks = [self.convert_external_task_input_to_external_task(external_task_input=sub_task) for sub_task in external_task_input.sub_tasks]

        return result

    def convert(self) -> [ExternalTask]:
        return [self.convert_external_task_input_to_external_task(external_task_input=external_task_input) for external_task_input in self.external_task_inputs]
