from Entities.ExternalTask.ExternalTask import ExternalTask
from Entities.ExternalTask.ExternalTaskEffort import ExternalTaskEffort
from Entities.Skill.AbilityEnum import AbilityEnum
from Repository.ExternalTaskRepository.ExternalTaskRepository import ExternalTaskRepository


class FakeExternalTaskRepository(ExternalTaskRepository):

    def __init__(self):
        self.external_tasks: [ExternalTask] = [self.generate_first_task(), self.generate_second_task()]

    def generate_first_task(self) -> ExternalTask:
        task_1 = ExternalTask(id='CR-1', name='Change Request 1', system='')
        task_1.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=80.0),
            ExternalTaskEffort(ability=AbilityEnum.INTEGRATION_TESTING, hours=40.0),
            ExternalTaskEffort(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=80.0)
        ]

        task_1_1 = ExternalTask(id='SYSCR-1.1', name='System Change Request 1.1', system='SYS-1')
        task_1_1.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=80.0),
            ExternalTaskEffort(ability=AbilityEnum.DEVELOPMENT, hours=40.0),
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_TESTING, hours=80.0)
        ]

        task_1_1_1 = ExternalTask(id='SYSAN-1.1.1', name='System Analysis 1.1', system='SYS-1')
        task_1_1_1.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0)
        ]
        task_1_1_2 = ExternalTask(id='DEV-1.1.1', name='Development 1.1', system='SYS-1')
        task_1_1_2.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.DEVELOPMENT, hours=120.0)
        ]

        task_1_1_3 = ExternalTask(id='SYSTEST-1.1.1', name='System Testing 1.1', system='SYS-1')
        task_1_1_3.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]
        task_1_1.sub_tasks = [task_1_1_1, task_1_1_2, task_1_1_3]

        task_1_2 = ExternalTask(id='SYSCR-1.2', name='System Change Request 1.2', system='SYS-2')
        task_1_2.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=400.0),
            ExternalTaskEffort(ability=AbilityEnum.DEVELOPMENT, hours=1200),
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_TESTING, hours=400.0)
        ]
        task_1.sub_tasks = [
            task_1_1,
            task_1_2
        ]

        return task_1

    def generate_second_task(self) -> ExternalTask:
        task_2 = ExternalTask(id='CR-4', name='Change Request 4', system='')
        task_2.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=8.0),
            ExternalTaskEffort(ability=AbilityEnum.INTEGRATION_TESTING, hours=2.0),
            ExternalTaskEffort(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=10.0)
        ]
        task_2_1 = ExternalTask(id='SYSCR-4.1', name='System Change Request 4.1', system='SYS-1')
        task_2_1.efforts = [
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0),
            ExternalTaskEffort(ability=AbilityEnum.DEVELOPMENT, hours=120.0),
            ExternalTaskEffort(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]
        task_2.sub_tasks = [
            task_2_1
        ]

        return task_2

    def get_external_task_by_id(self, external_task_id: str) -> ExternalTask:
        external_tasks = [external_task for external_task in self.external_tasks if external_task.id == external_task_id]

        if len(external_tasks) == 1:
            return external_tasks[0]
        else:
            raise ValueError('FakeExternalTaskRepository get_external_task_by_id expected to find 1 task with id {}, but {} found.'.format(external_task_id, len(external_tasks)))

    def has_external_task_with_id(self, external_task_id: str) -> bool:
        external_tasks = [external_task for external_task in self.external_tasks if external_task.id == external_task_id]

        has_exactly_one_task_with_id = len(external_tasks) == 1

        return has_exactly_one_task_with_id