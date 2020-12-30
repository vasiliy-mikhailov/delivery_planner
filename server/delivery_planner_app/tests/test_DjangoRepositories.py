from django.test import TestCase

# Create your tests here.
from Entities.ExternalTask.ExternalTask import ExternalTask
from Entities.ExternalTask.ExternalTaskEffort import ExternalTaskEffort
from Entities.Skill.AbilityEnum import AbilityEnum
from Repository.ExternalTaskRepository.DbExternalTaskRepository import DbExternalTaskRepository


class DbExternalTaskRepositoryTestCase(TestCase):

    def test_db_external_task_repository_does_not_find_non_existent_record(self):
        db_external_task_repository = DbExternalTaskRepository()

        non_existent_task_id = 'NON-EXISTENT_TASK-ID'

        task_exists = db_external_task_repository.has_external_task_with_id(external_task_id=non_existent_task_id)

        self.assertFalse(task_exists)

    def test_db_external_task_repository_creates_record(self):
        db_external_task_repository = DbExternalTaskRepository()

        external_task_1 = ExternalTask(
            id='CR-1',
            name='Change Request 1',
            system='',
        )

        external_task_1.efforts = [
            ExternalTaskEffort(
                ability=AbilityEnum.SYSTEM_ANALYSIS,
                hours=8
            ),
            ExternalTaskEffort(
                ability=AbilityEnum.DEVELOPMENT,
                hours=80
            )
        ]

        external_task_1_1 = ExternalTask(
            id='SYS-CR-1.1',
            name='System Change Request 1.1',
            system='SYS-1',
        )

        external_task_1_2 = ExternalTask(
            id='SYS-CR-1.2',
            name='System Change Request 1.2',
            system='SYS-2',
        )

        external_task_1.sub_tasks = [external_task_1_1, external_task_1_2]

        db_external_task_repository.save(external_task=external_task_1)

        external_task_1_from_db = db_external_task_repository.get_external_task_by_id(external_task_id=external_task_1.id)

        self.assertEquals(external_task_1, external_task_1_from_db)

