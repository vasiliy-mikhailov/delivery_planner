from Inputs.PlanInput import PlanInput
from Inputs.TaskIdInput import TaskIdInput
from Inputs.TaskInput import  TaskInput
from datetime import date
from Inputs.ExistingResourceInput import ExistingResourceInput
from Entities.Skill.AbilityEnum import AbilityEnum
from Inputs.EffortInput import EffortInput
from Inputs.CapacityInput import CapacityInput
from Inputs.PlannedResourceInput import PlannedResourceInput
from Inputs.VacationInput import VacationInput

class FakePlanReader:

    def generate_first_task(self) -> TaskInput:
        task_1 = TaskInput(id='CR-1', name='Change Request 1', system='', business_line='BL-1')
        task_1.efforts = [
            EffortInput(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=80.0),
            EffortInput(ability=AbilityEnum.INTEGRATION_TESTING, hours=40.0),
            EffortInput(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=80.0)
        ]

        task_1_1 = TaskInput(id='SYSCR-1.1', name='System Change Request 1.1', system='SYS-1', business_line='BL-1')
        task_1_1.efforts = [
        ]

        task_1_1_1 = TaskInput(id='SYSAN-1.1.1', name='System Analysis 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_1.efforts = [
            EffortInput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0)
        ]
        task_1_1_2 = TaskInput(id='DEV-1.1.1', name='Development 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_2.efforts = [
            EffortInput(ability=AbilityEnum.DEVELOPMENT, hours=120.0)
        ]
        task_1_1_2.predecessors = [task_1_1_1]

        task_1_1_3 = TaskInput(id='SYSTEST-1.1.1', name='System Testing 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_3.efforts = [
            EffortInput(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]
        task_1_1_3.predecessors = [task_1_1_2]

        task_1_1.sub_tasks = [task_1_1_1, task_1_1_2, task_1_1_3]

        task_1_2 = TaskInput(id='SYSCR-1.2', name='System Change Request 1.2', system='SYS-2', business_line='BL-1')
        task_1_2.efforts = [
            EffortInput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=400.0),
            EffortInput(ability=AbilityEnum.DEVELOPMENT, hours=1200),
            EffortInput(ability=AbilityEnum.SYSTEM_TESTING, hours=400.0)
        ]
        task_1.sub_tasks = [
            task_1_1,
            task_1_2
        ]

        return task_1

    def generate_second_task(self) -> TaskInput:
        task_2 = TaskInput(id='CR-2', name='Change Request 2', system='', business_line='BL-2')
        task_2.efforts = [
            EffortInput(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=8.0),
            EffortInput(ability=AbilityEnum.INTEGRATION_TESTING, hours=2.0),
            EffortInput(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=10.0)
        ]
        task_2_1 = TaskInput(id='SYSCR-2.1', name='System Change Request 2.1', system='SYS-1', business_line='BL-2')
        task_2_1.efforts = [
            EffortInput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0),
            EffortInput(ability=AbilityEnum.DEVELOPMENT, hours=120.0),
            EffortInput(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]
        task_2.sub_tasks = [
            task_2_1
        ]

        return task_2

    def generate_existing_resource(
            self,
            id: str,
            name: str,
            business_line: str,
            calendar: str,
            hours_per_day: float,
            capacity_per_day: [CapacityInput]
    ) -> ExistingResourceInput:
        existing_resource = ExistingResourceInput(
                id=id,
                name=name,
                business_line=business_line,
                calendar=calendar,
                hours_per_day=hours_per_day
        )
        existing_resource.capacity_per_day = capacity_per_day

        return existing_resource

    def generate_existing_resources(self):
        existing_resources = [
            self.generate_existing_resource(
                id='SOLAR-1',
                name='Архитектор А.Р.',
                business_line='BL-1',
                calendar='RU',
                hours_per_day=7.0,
                capacity_per_day=[
                    CapacityInput('', ability=AbilityEnum.SOLUTION_ARCHITECTURE, efficiency=1.0)
                ]
            ),
            self.generate_existing_resource(
                id='PM-1',
                name='Рукпроекта Р.П.',
                business_line='BL-1',
                calendar='RU',
                hours_per_day=7.0,
                capacity_per_day=[
                    CapacityInput('', ability=AbilityEnum.PROJECT_MANAGEMENT, efficiency=1.0)
                ]
            ),
            self.generate_existing_resource(
                id='SYSAN-1',
                name='Аналитик С.А.',
                business_line='BL-1',
                calendar='RU',
                hours_per_day=7.0,
                capacity_per_day=[
                    CapacityInput('SYS-1', ability=AbilityEnum.SYSTEM_ANALYSIS, efficiency=1.0),
                    CapacityInput('SYS-2', ability=AbilityEnum.SYSTEM_ANALYSIS, efficiency=0.5)
                ]
            ),
            self.generate_existing_resource(
                id='SYSDEV-1',
                name='Разработчик С.А.',
                business_line='BL-1',
                calendar='BY',
                hours_per_day=7.0,
                capacity_per_day=[
                    CapacityInput('SYS-1', ability=AbilityEnum.DEVELOPMENT, efficiency=1.0),
                    CapacityInput('SYS-2', ability=AbilityEnum.DEVELOPMENT, efficiency=0.5)
                ]
            ),
            self.generate_existing_resource(
                id='SYSTEST-1',
                name='Тестировщик С.А.',
                business_line='BL-1',
                calendar='RU',
                hours_per_day=7.0,
                capacity_per_day=[
                    CapacityInput('SYS-1', ability=AbilityEnum.SYSTEM_TESTING, efficiency=1.0),
                    CapacityInput('SYS-2', ability=AbilityEnum.SYSTEM_TESTING, efficiency=0.5)
                ]
            ),
            self.generate_existing_resource(
                id='INNTEST-1',
                name='Тестировщик И.А.',
                business_line='BL-1',
                calendar='BY',
                hours_per_day=7.0,
                capacity_per_day=[
                    CapacityInput('', ability=AbilityEnum.INTEGRATION_TESTING, efficiency=1.0)
                ]
            ),
            self.generate_existing_resource(
                id='BUS-1',
                name='Владелец П.А.',
                business_line='BL-1',
                calendar='RU',
                hours_per_day=2.0,
                capacity_per_day=[
                    CapacityInput('', ability=AbilityEnum.PRODUCT_OWNERSHIP, efficiency=1.0)
                ]
            ),
        ]

        return existing_resources

    def generate_planned_resources(self):
        planned_resource_1 = PlannedResourceInput(
            id='PLANRES-1',
            name='5 разработчиков системы 1',
            business_line='BL-1',
            start_date=date(2021, 1, 1),
            full_power_in_month=5.0,
            calendar='RU',
            hours_per_day=56.0
        )
        planned_resource_1.capacity_per_day = [
            CapacityInput(system='SYS-1', ability=AbilityEnum.DEVELOPMENT, efficiency=1.0)
        ]
        planned_resource_2 = PlannedResourceInput(
            id='PLANRES-2',
            name='5 разработчиков системы 2',
            business_line='BL-1',
            start_date=date(2020, 9, 1),
            full_power_in_month=5.0,
            calendar='RU',
            hours_per_day=56.0
        )
        planned_resource_2.capacity_per_day = [
            CapacityInput(system='SYS-2', ability=AbilityEnum.DEVELOPMENT, efficiency=1.0)
        ]
        result = [
            planned_resource_1,
            planned_resource_2
        ]
        return result

    def generate_vacations(self):
        vacation_1 = VacationInput(resource_id='SOLAR-1', start_date=date(2020, 10, 14), end_date=date(2020, 10, 15))
        return [vacation_1]

    def generate_task_ids_to_add(self):
        return [
            TaskIdInput(id='CR-4'),
        ]

    def read(self) -> PlanInput:
        result = PlanInput(start_date=date(2020, 10, 5), end_date=date(2021, 2, 5))
        task_1 = self.generate_first_task()
        task_2 = self.generate_second_task()
        result.tasks = [
            task_1, task_2
        ]
        result.existing_resources = self.generate_existing_resources()
        result.planned_resources = self.generate_planned_resources()
        result.vacations = self.generate_vacations()
        result.task_ids_to_add = self.generate_task_ids_to_add()

        return result