from Inputs.ExternalTaskInput import ExternalTaskInput
from Interactors.ExternalTasksToExternalTaskOutputsConverter import ExternalTasksToExternalTaskOutputsConverter
from Interactors.PlannerInteractor.ExternalTaskInputsToEntitiesConverter import ExternalTaskInputsToEntitiesConverter
from Outputs.ExternalTaskOutput import ExternalTaskOutput


class PullExternalTasksAndCreateExcelInteractor:

    def __init__(self, external_task_inputs: [ExternalTaskInput]):
        self.external_task_inputs: [ExternalTaskInput] = external_task_inputs

    def interact(self) -> [ExternalTaskOutput]:
        external_task_inputs = self.external_task_inputs
        external_task_inputs_to_entities_converter = ExternalTaskInputsToEntitiesConverter(external_task_inputs=external_task_inputs)
        external_tasks = external_task_inputs_to_entities_converter.convert()
        convert_external_tasks_to_external_task_outputs = ExternalTasksToExternalTaskOutputsConverter(external_tasks=external_tasks)
        result = convert_external_tasks_to_external_task_outputs.convert()
        return result