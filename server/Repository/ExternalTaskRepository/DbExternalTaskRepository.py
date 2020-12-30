from Entities.ExternalTask.ExternalTask import ExternalTask
from Entities.ExternalTask.ExternalTaskEffort import ExternalTaskEffort
from Entities.Skill.AbilityEnum import AbilityEnum
from delivery_planner_app.models import ExternalTaskDAO, ExternalTaskEffortLeftDAO, AbilityEnumDAO


class DbExternalTaskRepository:

    ABILITY_ENUM_DAO_STR_TO_ABILITY_ENUM = {
        'SYSTEM_ANALYSIS': AbilityEnum.SYSTEM_ANALYSIS,
        'DEVELOPMENT': AbilityEnum.DEVELOPMENT,
        'SYSTEM_TESTING': AbilityEnum.SYSTEM_TESTING
    }

    ABILITY_ENUM_TO_ABILITY_ENUM_DAO = {
        AbilityEnum.SYSTEM_ANALYSIS: 'SYSTEM_ANALYSIS',
        AbilityEnum.DEVELOPMENT: 'DEVELOPMENT',
        AbilityEnum.SYSTEM_TESTING: 'SYSTEM_TESTING'
    }

    def convert_ability_enum_dao_to_ability_enum(self, ability_enum_dao: AbilityEnumDAO) -> AbilityEnum:
        return self.ABILITY_ENUM_DAO_STR_TO_ABILITY_ENUM[ability_enum_dao]

    def convert_external_task_effort_left_dao_to_external_task_effort(self, external_task_efforts_left_dao: [ExternalTaskEffortLeftDAO]) -> ExternalTaskEffort:
        result = []

        for external_task_effort_left_dao in external_task_efforts_left_dao.all():
            ability_enum_dao_str = external_task_effort_left_dao.ability
            ability = self.convert_ability_enum_dao_to_ability_enum(ability_enum_dao=ability_enum_dao_str)
            hours = external_task_effort_left_dao.hours
            external_task_effort = ExternalTaskEffort(
                ability=ability,
                hours=hours
            )
            result.append(external_task_effort)

        return result

    def convert_external_task_dao_to_external_task(self, external_task_dao: ExternalTaskDAO) -> ExternalTask:
        result = ExternalTask(
            id=external_task_dao.id,
            name=external_task_dao.name,
            system=external_task_dao.system,
        )

        external_task_efforts_left_dao = external_task_dao.externaltaskeffortleftdao_set

        result.efforts = self.convert_external_task_effort_left_dao_to_external_task_effort(external_task_efforts_left_dao=external_task_efforts_left_dao)

        external_task_dao_sub_tasks = external_task_dao.externaltaskdao_set.all()
        result.sub_tasks = [self.convert_external_task_dao_to_external_task(external_task_dao=sub_task) for sub_task in external_task_dao_sub_tasks]

        return result

    def get_external_task_by_id(self, external_task_id: str) -> ExternalTask:
        external_tasks_dao = ExternalTaskDAO.objects.filter(id=external_task_id, parent=None)

        external_tasks_dao_quantity = external_tasks_dao.count()

        if external_tasks_dao_quantity == 1:
            external_task_dao = external_tasks_dao[0]
            return self.convert_external_task_dao_to_external_task(external_task_dao=external_task_dao)
        else:
            raise ValueError('DbExternalTaskRepository get_external_task_by_id expected exactly one external task with id {}, but {} found'.format(external_task_id, external_tasks_dao_quantity))

    def has_external_task_with_id(self, external_task_id: str) -> bool:
        external_tasks_dao = ExternalTaskDAO.objects.filter(id=external_task_id, parent=None)

        return external_tasks_dao.count() == 1

    def convert_ability_enum_to_ability_enum_dao(self, ability: AbilityEnum):
        return self.ABILITY_ENUM_TO_ABILITY_ENUM_DAO[ability]

    def convert_external_task_efforts_to_external_task_effort_left_dao_and_save(self, external_task_dao: ExternalTaskDAO, external_task_efforts: [ExternalTaskEffort]) -> [ExternalTaskEffortLeftDAO]:
        for external_task_effort in external_task_efforts:
            ability = self.convert_ability_enum_to_ability_enum_dao(ability=external_task_effort.ability)
            hours = external_task_effort.hours
            effort_dao = ExternalTaskEffortLeftDAO(
                ability=ability,
                hours=hours,
                external_task=external_task_dao
            )
            effort_dao.save()

    def convert_external_task_to_external_task_dao_and_save(self, external_task: ExternalTask, parent_external_task: ExternalTaskDAO) -> ExternalTaskDAO:
        external_task_dao = ExternalTaskDAO(
            id=external_task.id,
            name=external_task.name,
            system=external_task.system
        )

        external_task_dao.parent = parent_external_task

        external_task_dao.save()

        self.convert_external_task_efforts_to_external_task_effort_left_dao_and_save(external_task_dao=external_task_dao, external_task_efforts=external_task.efforts)

        for sub_task in external_task.sub_tasks:
            self.convert_external_task_to_external_task_dao_and_save(external_task=sub_task, parent_external_task=external_task_dao)

    def save(self, external_task: ExternalTask):
        self.convert_external_task_to_external_task_dao_and_save(external_task=external_task, parent_external_task=None)

    def get_all(self) -> [ExternalTask]:
        first_level_external_tasks_dao = ExternalTaskDAO.objects.filter(parent=None)

        return [self.convert_external_task_dao_to_external_task(external_task_dao=external_task_dao) for external_task_dao in first_level_external_tasks_dao]