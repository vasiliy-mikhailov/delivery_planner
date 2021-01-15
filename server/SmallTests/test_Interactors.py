import os
from math import isclose
from Entities.Plan.Plan import Plan
from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Resource.Calendar.VacationCalendar import VacationCalendar
from Entities.Resource.Capacity.Capacities import Capacities
from Entities.Resource.EfficiencyInTime.LinearGrowthEfficiency import LinearGrowthEfficiency
from Entities.Resource.SimpleResource import SimpleResource
from Entities.Skill.Skill import Skill
from Entities.Task.FinishStartConstrainedTask import FinishStartConstrainedTask
from Entities.Task.SimpleTask import SimpleTask
from Entities.Skill.AbilityEnum import AbilityEnum
from Inputs.TaskIdInput import TaskIdInput
from Interactors.PlannerInteractor.PlanInputToEntitiesConverter import PlanInputToEntitiesConverter
from Interactors.PlannerInteractor.PlannerInteractor import PlannerInteractor
from datetime import date
from Inputs.PlanInput import PlanInput
from Outputs.HightlightOutput import HighlightOutput
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanOutput import ResourceCalendarPlanOutput
from SmallTests.FakeExternalTaskRepository import FakeExternalTaskRepository
from SmallTests.FakePlannerInteractor import FakePlanner
from SmallTests.FakePlanReader import FakePlanReader
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationOutput import ResourceUtilizationOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyOutput import TaskResourceSupplyOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyRowOutput import TaskResourceSupplyRowOutput
from SmallTests.FakeTaskIdInputReader import FakeTaskIdInputReader


def test_planner_holds_attributes():
    plan_input = PlanInput(start_date=date(2020, 10, 5), end_date=date(2021, 2, 5))
    external_task_repository = FakeExternalTaskRepository()
    sut = PlannerInteractor(plan_input=plan_input, external_task_repository=external_task_repository)
    assert isinstance(sut.plan, Plan)
    assert sut.plan.start_date == date(2020, 10, 5)
    assert sut.plan.end_date == date(2021, 2, 5)
    assert sut.external_task_repository == external_task_repository

def test_planner_returns_empty_plan_when_there_are_no_tasks_and_no_resources():
    plan_input = PlanInput(start_date=date(2020, 10, 5), end_date=date(2021, 2, 5))
    external_task_repository = FakeExternalTaskRepository()
    sut = PlannerInteractor(plan_input=plan_input, external_task_repository=external_task_repository)

    plan_output = sut.interact()
    assert plan_output is not None
    assert isinstance(plan_output, PlanOutput)
    assert len(plan_output.task_resource_supply.rows) == 0


def test_fake_planner_generates_resource_utilization():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    assert plan_output is not None
    assert isinstance(plan_output, PlanOutput)
    assert isinstance(plan_output.task_resource_supply, TaskResourceSupplyOutput)
    assert len(plan_output.task_resource_supply.rows) == 2
    assert isinstance(plan_output.task_resource_supply.rows[0], TaskResourceSupplyRowOutput)

    assert isinstance(plan_output.resource_utilization, ResourceUtilizationOutput)


def test_convert_plan_input_to_entities_converts_plan_input_to_entities():
    fake_plan_reader = FakePlanReader()
    plan_input = fake_plan_reader.read()

    sut = PlanInputToEntitiesConverter(plan_input=plan_input)

    existing_resources = sut.convert_existing_resources_to_entities()
    assert len(existing_resources) == 7
    existing_resource_0 = existing_resources[0]
    assert existing_resource_0.id == 'SOLAR-1'
    assert existing_resource_0.name == 'Архитектор А.Р.'
    assert existing_resource_0.work_date_start == plan_input.start_date
    assert existing_resource_0.work_date_end == plan_input.end_date
    assert existing_resource_0.business_line == 'BL-1'
    assert isinstance(existing_resource_0.capacities, Capacities)
    assert isinstance(existing_resource_0.capacities.calendar, VacationCalendar)
    assert not existing_resource_0.capacities.calendar.is_working_day(date(2020, 10, 14))
    assert existing_resource_0.get_remaining_work_hours() == 567
    assert len(existing_resource_0.capacities.capacity_list) == 1
    assert existing_resource_0.capacities.get_work_hours_for_date(date=date(2020, 10, 5)) == 7
    assert existing_resource_0.capacities.get_efficiency_for_date_and_skill(
        date=date(2020, 10, 5),
        skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE)
    ) == 1

    existing_resource_1 = existing_resources[1]
    assert existing_resource_1.id == 'PM-1'
    assert existing_resource_1.name == 'Рукпроекта Р.П.'
    assert existing_resource_1.work_date_start == plan_input.start_date
    assert existing_resource_1.work_date_end == plan_input.end_date
    assert existing_resource_1.business_line == 'BL-1'
    assert isinstance(existing_resource_1.capacities, Capacities)
    assert isinstance(existing_resource_1.capacities.calendar, VacationCalendar)
    assert existing_resource_1.capacities.calendar.is_working_day(date(2020, 10, 14))
    assert existing_resource_1.get_remaining_work_hours() == 581
    assert len(existing_resource_1.capacities.capacity_list) == 1
    assert existing_resource_1.capacities.get_efficiency_for_date_and_skill(
        date=date(2020, 10, 5),
        skill=Skill(system='', ability=AbilityEnum.PROJECT_MANAGEMENT)
    ) == 1

    planned_resources = sut.convert_planned_resources_to_entities()
    assert len(planned_resources) == 2
    planned_resource_0 = planned_resources[0]
    assert planned_resource_0.id == 'PLANRES-1'
    assert planned_resource_0.business_line == 'BL-1'
    assert planned_resource_0.work_date_start == date(2021, 1, 1)
    assert isinstance(planned_resource_0.capacities.calendar, RussianCalendar)
    assert isinstance(planned_resource_0.capacities.efficiency_in_time, LinearGrowthEfficiency)
    assert len(planned_resource_0.capacities.capacity_list) == 1
    assert isclose(
        planned_resource_0.capacities.get_efficiency_for_date_and_skill(
            date=date(2021, 2, 1),
            skill=Skill(system='SYS-1', ability=AbilityEnum.DEVELOPMENT)
        ), 0.21, rel_tol=0.01
    )

    planned_resource_1 = planned_resources[1]
    assert planned_resource_1.id == 'PLANRES-2'
    assert planned_resource_1.business_line == 'BL-1'
    assert planned_resource_1.work_date_start == date(2020, 10, 5)
    assert len(planned_resource_1.capacities.capacity_list) == 1
    assert planned_resource_1.capacities.get_efficiency_for_date_and_skill(
        date=date(2021, 2, 1),
        skill=Skill(system='SYS-2', ability=AbilityEnum.DEVELOPMENT),
    ) == 1

    resources = existing_resources + planned_resources

    tasks = sut.convert_task_inputs_to_tasks(task_inputs=plan_input.tasks, resources=resources)

    assert len(tasks) == 2

    task_0 = tasks[0]
    assert isinstance(task_0, SimpleTask)
    assert task_0.get_id() == 'CR-1'
    assert task_0.get_name() == 'Change Request 1'
    assert task_0.get_business_line() == 'BL-1'
    assert len(task_0.get_remaining_efforts_ignoring_sub_tasks().effort_entries) == 3
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(
        system='',
        ability=AbilityEnum.SOLUTION_ARCHITECTURE
    )) == 80
    assert len(task_0.get_direct_sub_tasks()) == 2
    task_0_0 = task_0.get_direct_sub_tasks()[0]
    assert len(task_0_0.get_direct_sub_tasks()) == 3
    task_0_0_0 = task_0_0.get_direct_sub_tasks()[0]
    assert isinstance(task_0_0_0, SimpleTask)
    task_0_0_1 = task_0_0.get_direct_sub_tasks()[1]
    assert isinstance(task_0_0_1, FinishStartConstrainedTask)
    assert task_0_0_1.predecessors == [task_0_0_0]
    task_0_0_2 = task_0_0.get_direct_sub_tasks()[2]
    assert isinstance(task_0_0_2, FinishStartConstrainedTask)
    assert task_0_0_2.predecessors == [task_0_0_1]


def test_planner_simulates_execution():
    fake_plan_reader = FakePlanReader()
    plan_input = fake_plan_reader.read()
    external_task_repository = FakeExternalTaskRepository()
    sut = PlannerInteractor(plan_input=plan_input, external_task_repository=external_task_repository)

    sut.convert_input_to_entities()
    assert len(sut.plan.tasks) == 2
    assert len(sut.plan.resources) == 9
    sut.simulate_resources_worked_on_task()

    assert len(sut.plan.tasks) == 2
    task_0: SimpleTask = sut.plan.tasks[0]
    assert isclose(task_0.get_remaining_efforts_hours(), 1211, rel_tol=0.01)
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE)) == 0
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='SYS-1', ability=AbilityEnum.SYSTEM_ANALYSIS)) == 0
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='SYS-1', ability=AbilityEnum.DEVELOPMENT)) == 0
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='SYS-1', ability=AbilityEnum.SYSTEM_TESTING)) == 0
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='SYS-2', ability=AbilityEnum.SYSTEM_ANALYSIS)) == 129.5
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='SYS-2', ability=AbilityEnum.DEVELOPMENT)) == 952
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='SYS-2', ability=AbilityEnum.SYSTEM_TESTING)) == 129.5
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.INTEGRATION_TESTING)) == 0
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.PRODUCT_OWNERSHIP)) == 0
    assert task_0.get_remaining_efforts_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.PROJECT_MANAGEMENT)) == 0

    task_1: SimpleTask = sut.plan.tasks[1]
    assert task_1.get_remaining_efforts_hours() == 220

    resource_0: SimpleResource = sut.plan.resources[0]
    assert resource_0.get_remaining_work_hours() == 487

    resource_1: SimpleResource = sut.plan.resources[1]
    assert resource_1.get_remaining_work_hours() == 581

    resource_2: SimpleResource = sut.plan.resources[2]
    assert resource_2.get_remaining_work_hours() == 0


def test_planner_produces_output():
    fake_plan_reader = FakePlanReader()
    plan_input = fake_plan_reader.read()

    external_task_repository = FakeExternalTaskRepository()
    sut = PlannerInteractor(plan_input=plan_input, external_task_repository=external_task_repository)
    plan_output: PlanOutput = sut.interact()

    assert len(plan_output.task_resource_supply.rows) == 3
    row_0 = plan_output.task_resource_supply.rows[0]
    assert len(row_0.skill_resource_supply) == 9
    assert sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == '' and s.ability == AbilityEnum.SOLUTION_ARCHITECTURE]) == 1
    assert sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == 'SYS-1' and s.ability == AbilityEnum.SYSTEM_ANALYSIS]) == 1
    assert isclose(sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == 'SYS-2' and s.ability == AbilityEnum.SYSTEM_ANALYSIS]), 0.678, rel_tol=0.01)
    assert sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == 'SYS-1' and s.ability == AbilityEnum.DEVELOPMENT]) == 1
    assert isclose(sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == 'SYS-2' and s.ability == AbilityEnum.DEVELOPMENT]), 0.207, rel_tol=0.01)
    assert sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == 'SYS-1' and s.ability == AbilityEnum.SYSTEM_TESTING]) == 1
    assert isclose(sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == 'SYS-2' and s.ability == AbilityEnum.SYSTEM_TESTING]), 0.678, rel_tol=0.01)
    assert sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == '' and s.ability == AbilityEnum.INTEGRATION_TESTING]) == 1
    assert sum([s.supply_percent for s in row_0.skill_resource_supply if
                        s.system == '' and s.ability == AbilityEnum.PRODUCT_OWNERSHIP]) == 1

    assert isinstance(plan_output.resource_calendar_plan, ResourceCalendarPlanOutput)

    resource_calendar_plan = plan_output.resource_calendar_plan

    assert len(resource_calendar_plan.tasks) == 3
    task_0 = resource_calendar_plan.tasks[0]
    assert task_0.id == 'CR-1'
    assert task_0.name == 'Change Request 1'
    assert task_0.business_line == 'BL-1'
    assert task_0.start_date_or_empty_string == date(2020, 10, 5)
    assert task_0.start_date_highlight == HighlightOutput.REGULAR
    assert not task_0.end_date_or_empty_string
    assert task_0.end_date_highlight == HighlightOutput.ERROR
    assert task_0.initial_effort_hours == 2400
    assert isclose(task_0.assigned_effort_hours, 1189.0, abs_tol=0.01)
    assert isclose(task_0.planned_readiness, 0.495, abs_tol=0.01)
    assert task_0.planned_readiness_highlight == HighlightOutput.ERROR
    assert len(task_0.bottleneck_hints) == 5

    assert len(task_0.sub_tasks) == 2
    task_0_0 = task_0.sub_tasks[0]
    assert task_0_0.id == 'SYSCR-1.1'
    assert task_0_0.name == 'System Change Request 1.1'
    assert task_0_0.business_line == 'BL-1'
    assert task_0_0.start_date_or_empty_string == date(2020, 10, 5)
    assert task_0_0.start_date_highlight == HighlightOutput.REGULAR
    assert task_0_0.end_date_or_empty_string == date(2020, 11, 13)
    assert task_0_0.start_date_highlight == HighlightOutput.REGULAR
    assert task_0_0.initial_effort_hours == 200
    assert task_0_0.assigned_effort_hours == 200
    assert task_0_0.planned_readiness == 1.0
    assert task_0_0.planned_readiness_highlight == HighlightOutput.REGULAR

    assert len(task_0.groups) == 3
    group_0_0 = task_0.groups[0]
    assert group_0_0.system == ''
    assert group_0_0.ability == AbilityEnum.SOLUTION_ARCHITECTURE
    assert group_0_0.initial_hours == 80
    assert group_0_0.planned_hours == 80
    assert group_0_0.planned_readiness == 1
    assert group_0_0.highlight == HighlightOutput.REGULAR

    assert len(group_0_0.members) == 1
    member_0_0_0 = group_0_0.members[0]

    assert member_0_0_0.resource_id == 'SOLAR-1'
    assert member_0_0_0.resource_name == 'Архитектор А.Р.'
    assert member_0_0_0.highlight == HighlightOutput.REGULAR
    assert member_0_0_0.start_date_or_empty_string == date(2020, 10, 5)
    assert member_0_0_0.end_date_or_empty_string == date(2020, 10, 22)
    assert len(member_0_0_0.effort_decreases_by_date.values()) == 12
    assert member_0_0_0.effort_decrease_hours == 80
    assert sum(member_0_0_0.effort_decreases_by_date.values()) == 80

    assert len(task_0_0.sub_tasks) == 3
    task_0_0_0 = task_0_0.sub_tasks[0]
    assert task_0_0_0.id == 'SYSAN-1.1.1'
    assert task_0_0_0.name == 'System Analysis 1.1'
    assert task_0_0_0.business_line == 'BL-1'
    assert task_0_0_0.start_date_or_empty_string == date(2020, 10, 5)
    assert task_0_0_0.end_date_or_empty_string == date(2020, 10, 12)
    assert task_0_0_0.initial_effort_hours == 40
    assert task_0_0_0.assigned_effort_hours == 40
    assert task_0_0_0.planned_readiness == 1.0
    assert task_0_0_0.planned_readiness_highlight == HighlightOutput.REGULAR

    task_0_0_1 = task_0_0.sub_tasks[1]
    assert task_0_0_1.id == 'DEV-1.1.1'
    assert task_0_0_1.name == 'Development 1.1'
    assert task_0_0_1.business_line == 'BL-1'
    assert task_0_0_1.start_date_or_empty_string == date(2020, 10, 13)
    assert task_0_0_1.end_date_or_empty_string == date(2020, 11, 5)
    assert task_0_0_1.initial_effort_hours == 120
    assert task_0_0_1.assigned_effort_hours == 120
    assert task_0_0_1.planned_readiness == 1.0
    assert task_0_0_1.planned_readiness_highlight == HighlightOutput.REGULAR

    task_0_0_2 = task_0_0.sub_tasks[2]
    assert task_0_0_2.id == 'SYSTEST-1.1.1'
    assert task_0_0_2.name == 'System Testing 1.1'
    assert task_0_0_2.business_line == 'BL-1'
    assert task_0_0_2.start_date_or_empty_string == date(2020, 11, 6)
    assert task_0_0_2.end_date_or_empty_string == date(2020, 11, 13)
    assert task_0_0_2.initial_effort_hours == 40
    assert task_0_0_2.assigned_effort_hours == 40
    assert task_0_0_2.planned_readiness == 1.0
    assert task_0_0_2.planned_readiness_highlight == HighlightOutput.REGULAR

    task_2 = resource_calendar_plan.tasks[2]
    assert task_2.id == 'CR-4'
    assert task_2.name == 'Change Request 4'

    resource_utilization = plan_output.resource_utilization
    assert len(resource_utilization.resources) == 9

    resource_0 = resource_utilization.resources[0]
    assert resource_0.id == 'SOLAR-1'
    assert resource_0.name == 'Архитектор А.Р.'
    assert resource_0.business_line == 'BL-1'
    assert len(resource_0.utilization_by_date.values()) > 0
    assert isclose(sum(utilization_percent.value for utilization_percent in resource_0.utilization_by_date.values()), 54.42, rel_tol=0.01)

    assert len(resource_0.tasks) == 1
    task_0 = resource_0.tasks[0]
    assert len(task_0.hours_spent_by_day.values()) > 0
    assert sum(hours_spent for hours_spent in task_0.hours_spent_by_day.values()) == 80

def test_fake_task_id_input_reader_reads_data():
    fake_task_id_input_reader = FakeTaskIdInputReader()

    task_id_inputs = fake_task_id_input_reader.read()

    assert len(task_id_inputs) == 2
    assert isinstance(task_id_inputs[0], TaskIdInput)
    assert task_id_inputs[0].id == 'CR-1'

    assert isinstance(task_id_inputs[1], TaskIdInput)
    assert task_id_inputs[1].id == 'CR-4'









