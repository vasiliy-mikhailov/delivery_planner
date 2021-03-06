import datetime

import pytest

from Entities.ExternalTask.ExternalTask import ExternalTask
from Entities.Skill.AbilityEnum import AbilityEnum
from Inputs.PlanInput import PlanInput
from Inputs.TaskInput import TaskInput
from Repository.ExternalTaskRepository.ExcelExternalTaskRepository import ExcelExternalTaskRepository
from Repository.ExcelPlanReader import ExcelPlanReader
from SmallTests.FakeExternalTaskRepository import FakeExternalTaskRepository


def test_excel_reader_loads_excel():
    sut = ExcelPlanReader(file_name_or_io='./SmallTests/input_excels/Plan1.xlsx')
    plan_input = sut.read()

    assert isinstance(plan_input, PlanInput)
    assert plan_input.start_date == datetime.date(2020, 10, 5)
    assert plan_input.end_date == datetime.date(2021, 2, 5)
    assert len(plan_input.tasks) == 3

    tasks = plan_input.tasks

    assert isinstance(tasks[0], TaskInput)
    assert tasks[0].id == 'CR-1'
    assert tasks[0].business_line == 'BL-1'
    assert tasks[0].name == 'Заявка на доработку 1'

    assert len(tasks[0].sub_tasks) == 5

    task_0_0 = tasks[0].sub_tasks[0]
    assert task_0_0.id == 'SOLDES-1'
    assert task_0_0.business_line == 'BL-1'
    assert task_0_0.system == ''
    assert task_0_0.name == 'Разработка архитектуры решения'

    team_member_0_0_0 = task_0_0.team_members[0]
    assert team_member_0_0_0.system == ''
    assert team_member_0_0_0.ability == AbilityEnum.SOLUTION_ARCHITECTURE
    assert team_member_0_0_0.resource_ids_and_or_quantities == ['SOLAR-1']

    sub_tasks = tasks[0].sub_tasks

    task_0_1 = tasks[0].sub_tasks[1]
    assert isinstance(task_0_1, TaskInput)
    assert task_0_1.id == 'SYSCR-1.1'
    assert task_0_1.business_line == 'BL-1'
    assert task_0_1.system == 'SYS-1'
    assert task_0_1.name == 'Доработка системы 1.1'

    task_0_1_0 = task_0_1.sub_tasks[0]
    assert isinstance(task_0_1_0, TaskInput)
    assert task_0_1_0.id == 'SYSDES-1.1'
    assert task_0_1_0.business_line == 'BL-1'
    assert task_0_1_0.system == 'SYS-1'
    assert task_0_1_0.name == 'Низкоуровневое проектирование'
    assert len(task_0_1_0.predecessors) == 1
    assert isinstance(task_0_1_0.predecessors[0], TaskInput)
    assert task_0_1_0.predecessors[0].id == 'SOLDES-1'

    team_member_0_1_0_0 = task_0_1_0.team_members[0]
    assert team_member_0_1_0_0.system == 'SYS-1'
    assert team_member_0_1_0_0.ability == AbilityEnum.SYSTEM_ANALYSIS
    assert team_member_0_1_0_0.resource_ids_and_or_quantities == ['1']

    sub_tasks_1 = task_0_1.sub_tasks
    assert sum([x.hours for x in sub_tasks_1[0].efforts if x.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 30
    assert sum([x.hours for x in sub_tasks_1[1].efforts if x.ability == AbilityEnum.DEVELOPMENT]) == 100
    assert sum([x.hours for x in sub_tasks_1[2].efforts if x.ability == AbilityEnum.SYSTEM_TESTING]) == 30
    assert sub_tasks[2].id == 'SYSCR-1.2'
    sub_tasks_2 = sub_tasks[2].sub_tasks
    assert sum([x.hours for x in sub_tasks_2[0].efforts if x.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 300
    assert sum([x.hours for x in sub_tasks_2[1].efforts if x.ability == AbilityEnum.DEVELOPMENT]) == 1000
    assert sum([x.hours for x in sub_tasks_2[2].efforts if x.ability == AbilityEnum.SYSTEM_TESTING]) == 300

    assert isinstance(sub_tasks[1], TaskInput)

    assert isinstance(tasks[1], TaskInput)
    assert tasks[1].id == 'CR-2'
    assert tasks[1].business_line == 'BL-2'
    assert sum([x.hours for x in tasks[1].efforts if x.ability == AbilityEnum.SOLUTION_ARCHITECTURE]) == 8
    assert sum([x.hours for x in tasks[1].efforts if x.ability == AbilityEnum.INTEGRATION_TESTING]) == 0
    assert sum([x.hours for x in tasks[1].efforts if x.ability == AbilityEnum.PRODUCT_OWNERSHIP]) == 10
    assert len(tasks[1].sub_tasks) == 1
    sub_tasks = tasks[1].sub_tasks
    assert isinstance(sub_tasks[0], TaskInput)
    assert sub_tasks[0].id == 'SYSCR-2.1'
    assert sum([x.hours for x in sub_tasks[0].efforts if x.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 40
    assert sum([x.hours for x in sub_tasks[0].efforts if x.ability == AbilityEnum.DEVELOPMENT]) == 120
    assert sum([x.hours for x in sub_tasks[0].efforts if x.ability == AbilityEnum.SYSTEM_TESTING]) == 40

    assert len(plan_input.existing_resources) == 8

    resource_0 = plan_input.existing_resources[0]
    assert resource_0.id == 'SOLAR-1'
    assert resource_0.name == 'Архитектор А.Р.'
    assert resource_0.business_line == 'BL-1'
    assert resource_0.calendar == 'RU'
    assert resource_0.hours_per_day == 7
    assert len(resource_0.capacity_per_day) == 1
    assert sum([x.efficiency for x in resource_0.capacity_per_day]) == 1

    resource_2 = plan_input.existing_resources[2]
    assert resource_2.id == 'SYSAN-1'
    assert resource_2.name == 'Аналитик С.А.'
    assert resource_2.business_line == 'BL-1'
    assert resource_2.calendar == 'RU'
    assert resource_2.hours_per_day == 7
    assert len(resource_2.capacity_per_day) == 2
    assert sum([x.efficiency for x in resource_2.capacity_per_day]) == 1.5

    assert len(plan_input.planned_resources) == 1
    planned_resource_0 = plan_input.planned_resources[0]
    assert planned_resource_0.id == 'PLANRES-1'
    assert planned_resource_0.business_line == 'BL-1'
    assert planned_resource_0.start_date == datetime.date(2021, 1, 1)
    assert planned_resource_0.full_power_in_month == 5
    assert planned_resource_0.calendar == 'RU'
    assert planned_resource_0.hours_per_day == 56
    assert len(planned_resource_0.capacity_per_day) == 1
    assert planned_resource_0.capacity_per_day[0].system == 'SYS-1'
    assert planned_resource_0.capacity_per_day[0].ability == AbilityEnum.DEVELOPMENT
    assert planned_resource_0.capacity_per_day[0].efficiency == 1

    assert len(plan_input.temporary_resources) == 3
    temporary_resources_0 = plan_input.temporary_resources[0]
    assert temporary_resources_0.id == 'TEMPRES-1'
    assert temporary_resources_0.business_line == 'BL-1'
    assert temporary_resources_0.has_start_date == True
    assert temporary_resources_0.start_date == datetime.date(2021, 1, 1)
    assert temporary_resources_0.has_end_date == True
    assert temporary_resources_0.end_date == datetime.date(2021, 12, 31)
    assert temporary_resources_0.calendar == 'RU'
    assert temporary_resources_0.hours_per_day == 8
    assert len(temporary_resources_0.capacity_per_day) == 1
    assert temporary_resources_0.capacity_per_day[0].system == 'SYS-1'
    assert temporary_resources_0.capacity_per_day[0].ability == AbilityEnum.DEVELOPMENT
    assert temporary_resources_0.capacity_per_day[0].efficiency == 1

    temporary_resources_1 = plan_input.temporary_resources[1]
    assert temporary_resources_1.id == 'TEMPRES-2'
    assert temporary_resources_1.business_line == 'BL-1'
    assert temporary_resources_1.has_start_date == False
    assert temporary_resources_1.start_date == None
    assert temporary_resources_1.has_end_date == True
    assert temporary_resources_1.end_date == datetime.date(2021, 12, 31)
    assert temporary_resources_1.calendar == 'RU'
    assert temporary_resources_1.hours_per_day == 8
    assert len(temporary_resources_1.capacity_per_day) == 1
    assert temporary_resources_1.capacity_per_day[0].system == 'SYS-1'
    assert temporary_resources_1.capacity_per_day[0].ability == AbilityEnum.DEVELOPMENT
    assert temporary_resources_1.capacity_per_day[0].efficiency == 1

    temporary_resources_2 = plan_input.temporary_resources[2]
    assert temporary_resources_2.id == 'TEMPRES-3'
    assert temporary_resources_2.business_line == 'BL-1'
    assert temporary_resources_2.has_start_date == True
    assert temporary_resources_2.start_date == datetime.date(2021, 1, 1)
    assert temporary_resources_2.has_end_date == False
    assert temporary_resources_2.end_date == None
    assert temporary_resources_2.calendar == 'RU'
    assert temporary_resources_2.hours_per_day == 8
    assert len(temporary_resources_2.capacity_per_day) == 1
    assert temporary_resources_2.capacity_per_day[0].system == 'SYS-1'
    assert temporary_resources_2.capacity_per_day[0].ability == AbilityEnum.DEVELOPMENT
    assert temporary_resources_2.capacity_per_day[0].efficiency == 1

    assert len(plan_input.vacations) == 1
    assert plan_input.vacations[0].resource_id == 'SOLAR-1'
    assert plan_input.vacations[0].start_date == datetime.date(2020, 10, 14)
    assert plan_input.vacations[0].end_date == datetime.date(2020, 10, 15)

    task_2 = tasks[2]
    assert isinstance(task_2, TaskInput)
    assert task_2.id == 'CR-3'
    assert task_2.business_line == 'BL-1'
    assert task_2.system == 'SYS-1'

    team_member_2_0 = task_2.team_members[0]
    assert team_member_2_0.system == 'SYS-1'
    assert team_member_2_0.ability == AbilityEnum.DEVELOPMENT
    assert team_member_2_0.resource_ids_and_or_quantities == ['SYSDEV-1', '2']

def test_fake_external_data_repository_gets_by_id():
    fake_external_task_repository = FakeExternalTaskRepository()

    assert fake_external_task_repository.has_external_task_with_id(external_task_id='CR-1')
    cr_1 = fake_external_task_repository.get_external_task_by_id(external_task_id='CR-1')
    assert isinstance(cr_1, ExternalTask)

    assert fake_external_task_repository.has_external_task_with_id(external_task_id='CR-4')
    cr_4 = fake_external_task_repository.get_external_task_by_id('CR-4')
    assert isinstance(cr_4, ExternalTask)

    assert not fake_external_task_repository.has_external_task_with_id(external_task_id='NON-EXISTENT-ID')
    with pytest.raises(ValueError):
        _ = fake_external_task_repository.get_external_task_by_id('NON-EXISTENT-ID')

def test_excel_external_task_repository_holds_attributes():
    excel_task_repository_reader = ExcelExternalTaskRepository(file_name_or_io='./SmallTests/input_excels/external_tasks.xlsx')

    assert excel_task_repository_reader.file_name_or_io == './SmallTests/input_excels/external_tasks.xlsx'



