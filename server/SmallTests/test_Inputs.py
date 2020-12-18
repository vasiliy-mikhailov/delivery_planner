import math
from datetime import date

import pytest

from Inputs.TaskIdInput import TaskIdInput
from Inputs.TeamMemberInput import TeamMemberInput
from SmallTests.FakePlanReader import FakePlanReader
from Inputs.PlanInput import PlanInput
from Inputs.TaskInput import TaskInput
from Inputs.ExistingResourceInput import ExistingResourceInput
from Inputs.EffortInput import EffortInput
from Entities.Skill.AbilityEnum import AbilityEnum
from Inputs.CapacityInput import CapacityInput
from Inputs.PlannedResourceInput import PlannedResourceInput
from Inputs.VacationInput import VacationInput


def test_plan_input_holds_data():
    plan_input = PlanInput(start_date=date(2020, 10, 5), end_date=date(2021, 2, 5))
    assert plan_input.start_date == date(2020, 10, 5)
    assert plan_input.end_date == date(2021, 2, 5)
    assert len(plan_input.tasks) == 0
    assert len(plan_input.existing_resources) == 0
    assert len(plan_input.vacations) == 0
    assert len(plan_input.planned_resources) == 0
    assert len(plan_input.task_ids_to_add) == 0


def test_task_input_holds_data():
    task = TaskInput(id='CR-1', name='Change Request 1', system='SYS-1', business_line='BL-1')
    assert task.id == 'CR-1'
    assert task.name == 'Change Request 1'
    assert task.system == 'SYS-1'
    assert task.business_line == 'BL-1'
    assert len(task.efforts) == 0
    assert len(task.sub_tasks) == 0
    assert len(task.predecessors) == 0
    assert len(task.team_members) == 0


def test_task_input_raises_value_error_when_supplied_with_parameters_of_wrong_type():
    with pytest.raises(ValueError):
        _ = TaskInput(id=math.nan, name='Change Request 1', system='SYS-1', business_line='BL-1')

    with pytest.raises(ValueError):
        _ = TaskInput(id='CR-1', name=math.nan, system='SYS-1', business_line='BL-1')

    with pytest.raises(ValueError):
        _ = TaskInput(id='CR-1', name='Change Request 1', system=math.nan, business_line='BL-1')

    with pytest.raises(ValueError):
        _ = TaskInput(id='CR-1', name='Change Request 1', system='SYS-1', business_line=math.nan)


def test_ability_input_contains_all_abilitys():
    assert len(AbilityEnum) == 7


def test_existing_resource_holds_data():
    existing_resource = ExistingResourceInput(
        id='SOLAR-1',
        name='Архитектор А.Р.',
        business_line='BL-1',
        calendar='RU',
        hours_per_day=7.0
    )

    assert existing_resource.id == 'SOLAR-1'
    assert existing_resource.name == 'Архитектор А.Р.'
    assert existing_resource.business_line == 'BL-1'
    assert existing_resource.calendar == 'RU'
    assert existing_resource.hours_per_day == 7
    assert len(existing_resource.capacity_per_day) == 0


def test_effort_input_holds_data():
    ability_hours = EffortInput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=7.0)

    assert ability_hours.ability == AbilityEnum.SYSTEM_ANALYSIS
    assert ability_hours.hours == 7

def test_effort_input_raises_value_error_when_supplied_with_nan():
    with pytest.raises(ValueError):
        _ = EffortInput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=float('nan'))

def test_capacity_input_holds_data():
    capacity_input = CapacityInput(system='SYS-1', ability=AbilityEnum.SYSTEM_ANALYSIS, efficiency=7.0)

    assert capacity_input.system == 'SYS-1'
    assert capacity_input.ability == AbilityEnum.SYSTEM_ANALYSIS
    assert capacity_input.efficiency == 7

def test_capacity_input_raises_value_error_when_supplied_with_nan():
    with pytest.raises(ValueError):
        _ = CapacityInput(system='SYS-1', ability=AbilityEnum.SYSTEM_ANALYSIS, efficiency=float('nan'))

def test_planned_resource_holds_data():
    planned_resource = PlannedResourceInput(
        id='PLANRES-1',
        name='5 разработчиков системы 1',
        business_line='BL-1',
        start_date=date(2021, 1, 1),
        full_power_in_month=5,
        calendar='RU',
        hours_per_day=7.0
    )

    assert planned_resource.id == 'PLANRES-1'
    assert planned_resource.name == '5 разработчиков системы 1'
    assert planned_resource.business_line == 'BL-1'
    assert planned_resource.start_date == date(2021, 1, 1)
    assert planned_resource.full_power_in_month == 5
    assert planned_resource.calendar == 'RU'
    assert planned_resource.hours_per_day == 7
    assert len(planned_resource.capacity_per_day) == 0

def test_vacation_holds_data():
    vacation = VacationInput(resource_id='SOLAR-1', start_date=date(2020, 10, 14), end_date=date(2020, 10, 14))

    assert vacation.resource_id == 'SOLAR-1'
    assert vacation.start_date == date(2020, 10, 14)
    assert vacation.end_date == date(2020, 10, 14)

def test_fake_reader_loads_data():
    sut = FakePlanReader()
    plan_input = sut.read()

    assert isinstance(plan_input, PlanInput)
    assert plan_input.start_date == date(2020, 10, 5)
    assert plan_input.end_date == date(2021, 2, 5)
    assert len(plan_input.tasks) == 2

    tasks = plan_input.tasks

    assert isinstance(tasks[0], TaskInput)
    assert tasks[0].id == 'CR-1'
    assert tasks[0].business_line == 'BL-1'
    assert sum([x.hours for x in tasks[0].efforts if x.ability == AbilityEnum.SOLUTION_ARCHITECTURE]) == 80
    assert sum([x.hours for x in tasks[0].efforts if x.ability == AbilityEnum.INTEGRATION_TESTING]) == 40
    assert sum([x.hours for x in tasks[0].efforts if x.ability == AbilityEnum.PRODUCT_OWNERSHIP]) == 80
    assert len(tasks[0].sub_tasks) == 2
    task_0_0 = tasks[0].sub_tasks[0]
    assert isinstance(task_0_0, TaskInput)
    assert task_0_0.id == 'SYSCR-1.1'
    task_0_0_0 = task_0_0.sub_tasks[0]
    assert sum([x.hours for x in task_0_0_0.efforts if x.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 40
    task_0_0_1 = task_0_0.sub_tasks[1]
    assert sum([x.hours for x in task_0_0_1.efforts if x.ability == AbilityEnum.DEVELOPMENT]) == 120
    assert task_0_0_1.predecessors == [task_0_0_0]

    task_0_0_2 = task_0_0.sub_tasks[2]
    assert sum([x.hours for x in task_0_0_2.efforts if x.ability == AbilityEnum.SYSTEM_TESTING]) == 40
    assert task_0_0_2.predecessors == [task_0_0_1]
    task_0_1 = tasks[0].sub_tasks[1]
    assert task_0_1.id == 'SYSCR-1.2'
    assert sum([x.hours for x in task_0_1.efforts if x.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 400
    assert sum([x.hours for x in task_0_1.efforts if x.ability == AbilityEnum.DEVELOPMENT]) == 1200
    assert sum([x.hours for x in task_0_1.efforts if x.ability == AbilityEnum.SYSTEM_TESTING]) == 400

    assert isinstance(task_0_1, TaskInput)

    assert isinstance(tasks[1], TaskInput)
    assert tasks[1].id == 'CR-2'
    assert tasks[1].business_line == 'BL-2'
    assert sum([x.hours for x in tasks[1].efforts if x.ability == AbilityEnum.SOLUTION_ARCHITECTURE]) == 8
    assert sum([x.hours for x in tasks[1].efforts if x.ability == AbilityEnum.INTEGRATION_TESTING]) == 2
    assert sum([x.hours for x in tasks[1].efforts if x.ability == AbilityEnum.PRODUCT_OWNERSHIP]) == 10
    assert len(tasks[1].sub_tasks) == 1
    task_0_0 = tasks[1].sub_tasks
    assert isinstance(task_0_0[0], TaskInput)
    assert task_0_0[0].id == 'SYSCR-2.1'
    assert sum([x.hours for x in task_0_0[0].efforts if x.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 40
    assert sum([x.hours for x in task_0_0[0].efforts if x.ability == AbilityEnum.DEVELOPMENT]) == 120
    assert sum([x.hours for x in task_0_0[0].efforts if x.ability == AbilityEnum.SYSTEM_TESTING]) == 40

    assert len(plan_input.existing_resources) == 7

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

    assert len(plan_input.planned_resources) == 2
    planned_resource_0 = plan_input.planned_resources[0]
    assert planned_resource_0.id == 'PLANRES-1'
    assert planned_resource_0.business_line == 'BL-1'
    assert planned_resource_0.start_date == date(2021, 1, 1)
    assert planned_resource_0.full_power_in_month == 5
    assert planned_resource_0.calendar == 'RU'
    assert planned_resource_0.hours_per_day == 56
    assert len(planned_resource_0.capacity_per_day) == 1
    assert planned_resource_0.capacity_per_day[0].system == 'SYS-1'
    assert planned_resource_0.capacity_per_day[0].ability == AbilityEnum.DEVELOPMENT
    assert planned_resource_0.capacity_per_day[0].efficiency == 1

    assert len(plan_input.vacations) == 1
    assert plan_input.vacations[0].resource_id == 'SOLAR-1'
    assert plan_input.vacations[0].start_date == date(2020, 10, 14)
    assert plan_input.vacations[0].end_date == date(2020, 10, 15)

    assert len(plan_input.task_ids_to_add) == 1
    assert plan_input.task_ids_to_add[0].id == 'CR-4'

def test_team_member_input_holds_attributes():
    team_member = TeamMemberInput(system='SYS-1', ability=AbilityEnum.DEVELOPMENT, resource_ids_and_or_quantities=['1', 'foo@bar.com'])

    assert team_member.system == 'SYS-1'
    assert team_member.ability == AbilityEnum.DEVELOPMENT
    assert team_member.resource_ids_and_or_quantities == ['1', 'foo@bar.com']

def test_team_member_input_raises_exception_if_supplied_with_parameters_of_wrong_type():
    with pytest.raises(ValueError):
        _ = TeamMemberInput(
            system=math.nan,
            ability=AbilityEnum.DEVELOPMENT,
            resource_ids_and_or_quantities=['1', 'foo@bar.com']
        )

    with pytest.raises(ValueError):
        _ = TeamMemberInput(
            system='SYS-1',
            ability=math.nan,
            resource_ids_and_or_quantities=['1', 'foo@bar.com']
        )

    with pytest.raises(ValueError):
        _ = TeamMemberInput(
            system='SYS-1',
            ability=AbilityEnum.DEVELOPMENT,
            resource_ids_and_or_quantities=math.nan
        )

    with pytest.raises(ValueError):
        _ = TeamMemberInput(
            system='SYS-1',
            ability=AbilityEnum.DEVELOPMENT,
            resource_ids_and_or_quantities=[math.nan]
        )

def test_task_id_input_holds_data():
    task_id_input = TaskIdInput(id='CR-1')

    assert task_id_input.id == 'CR-1'

def test_task_id_init_raises_error_if_task_id_is_not_str():
    with pytest.raises(ValueError):
        _ = TaskIdInput(id=1)

