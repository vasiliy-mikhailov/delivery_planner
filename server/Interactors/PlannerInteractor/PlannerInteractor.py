from Entities.Plan.Plan import Plan
from Entities.RepositoryTask.ExternalTask import ExternalTask
from Entities.RepositoryTask.ExternalTaskEffort import ExternalTaskEffort
from Inputs.EffortInput import EffortInput
from Inputs.ExternalTaskInput import ExternalTaskInput
from Inputs.PlanInput import PlanInput
from Inputs.TaskInput import TaskInput
from Interactors.PlannerInteractor.ExternalTaskInputsToEntitiesConverter import ExternalTaskInputsToEntitiesConverter
from Interactors.PlannerInteractor.PlanOutputCreator import PlanOutputCreator
from Interactors.PlannerInteractor.PlanInputToEntitiesConverter import PlanInputToEntitiesConverter
from Outputs.PlanOutput import PlanOutput


class PlannerInteractor:

    def __init__(self, plan_input: PlanInput, external_task_inputs: [ExternalTaskInput]):
        self.plan_input: PlanInput = plan_input
        start_date = plan_input.start_date
        end_date = plan_input.end_date
        self.plan: Plan = Plan(start_date=start_date, end_date=end_date)
        self.external_task_inputs: [ExternalTaskInput] = external_task_inputs
        self.external_tasks: [ExternalTask] = []

    def convert_external_task_effort_to_effort_input(self, external_task_effort: ExternalTaskEffort) -> [EffortInput]:
        ability = external_task_effort.ability
        hours = external_task_effort.hours
        return EffortInput(ability=ability, hours=hours)

    def convert_external_task_to_task_input(self, external_task: ExternalTask) -> TaskInput:
        task_id = external_task.id
        task_name = external_task.name
        task_system = external_task.system
        task_business_line = external_task.business_line
        result = TaskInput(
            id=task_id,
            name=task_name,
            system=task_system,
            business_line=task_business_line
        )

        efforts = [self.convert_external_task_effort_to_effort_input(external_task_effort) for external_task_effort in external_task.efforts]

        result.efforts = efforts

        result.sub_tasks = [self.convert_external_task_to_task_input(sub_task) for sub_task in external_task.sub_tasks]

        return result

    def collect_external_tasks_by_id_recursive(self, external_tasks: [ExternalTask], task_id: str) -> [ExternalTask]:
        tasks_with_requested_id = [task for task in external_tasks if task.id == task_id]
        for task in external_tasks:
            tasks_with_requested_id = tasks_with_requested_id + self.collect_external_tasks_by_id_recursive(
                external_tasks=task.sub_tasks, task_id=task_id)

        return tasks_with_requested_id

    def has_external_task_with_id(self, external_task_id: str) -> bool:
        tasks_with_requested_id = self.collect_external_tasks_by_id_recursive(external_tasks=self.external_tasks, task_id=external_task_id)

        return len(tasks_with_requested_id) == 1

    def find_external_task_by_id(self, external_task_id: str) -> ExternalTask:
        tasks_with_requested_id = self.collect_external_tasks_by_id_recursive(external_tasks=self.external_tasks, task_id=external_task_id)

        if len(tasks_with_requested_id) == 1:
            return tasks_with_requested_id[0]
        else:
            raise ValueError('InMemoryTaskRepository get_task_by_id Expected exactly one task with id {}, but {} found.'.format(external_task_id, len(tasks_with_requested_id)))

    def convert_task_ids_to_task_inputs(self):
        task_ids_to_add = self.plan_input.task_ids_to_add

        result = []

        for task_id_input in task_ids_to_add:
            external_task = self.find_external_task_by_id(external_task_id=task_id_input.id)

            task_input = self.convert_external_task_to_task_input(external_task=external_task)

            result.append(task_input)

        return result

    def update_task_inputs_with_external_tasks_data(self):
        pass

    def convert_input_to_entities(self):
        plan_input_to_entities_converter = PlanInputToEntitiesConverter(plan_input=self.plan_input)
        resources = plan_input_to_entities_converter.convert_input_resources_to_entities()
        self.plan.resources = resources
        tasks = plan_input_to_entities_converter.convert_task_inputs_to_tasks(task_inputs=self.plan_input.tasks, resources=resources)
        self.plan.tasks = tasks

    def simulate_resources_worked_on_task(self):
        self.plan.plan_leveled()

    def create_output(self):
        plan = self.plan
        task_inputs = self.plan_input.tasks
        external_tasks = self.external_tasks
        output_creator = PlanOutputCreator(
            plan=plan,
            task_inputs=task_inputs,
            external_tasks=external_tasks
        )
        return output_creator.create_output()

    def interact(self) -> PlanOutput:
        external_task_inputs = self.external_task_inputs
        external_task_inputs_to_entities_converter = ExternalTaskInputsToEntitiesConverter(external_task_inputs=external_task_inputs)
        self.external_tasks = external_task_inputs_to_entities_converter.convert()
        tasks_to_add = self.convert_task_ids_to_task_inputs()
        self.plan_input.tasks = self.plan_input.tasks + tasks_to_add
        self.update_task_inputs_with_external_tasks_data()
        self.convert_input_to_entities()
        self.simulate_resources_worked_on_task()
        return self.create_output()

