from datetime import date

import math
import pytest

from Outputs.EffortOutput import EffortOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanBottleneckHintOutput import \
    ResourceCalendarPlanBottleneckHintOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanGroupOutput import ResourceCalendarPlanGroupOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanMemberOutput import ResourceCalendarPlanMemberOutput
from Outputs.ResourceLackOutput import ResourceLackOutput
from Outputs.TaskOutput import TaskOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyRowOutput import TaskResourceSupplyRowOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyOutput import TaskResourceSupplyOutput
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanOutput import ResourceCalendarPlanOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationOutput import ResourceUtilizationOutput
from Outputs.TaskResourceSupplyOutputs.SkillResourceSupplyOutput import SkillResourceSupplyOutput
from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.HightlightOutput import HighlightOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanTaskOutput import ResourceCalendarPlanTaskOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationPercentOutput import ResourceUtilizationPercentOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationResourceOutput import ResourceUtilizationResourceOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationTaskOutput import ResourceUtilizationTaskOutput
from Outputs.TeamMemberOutput import TeamMemberOutput


def test_plan_output_holds_attributes():
    plan_output = PlanOutput(start_date=date(2020, 10, 5), end_date=date(2020, 10, 20))
    assert plan_output.start_date == date(2020, 10, 5)
    assert plan_output.end_date == date(2020, 10, 20)
    assert len(plan_output.tasks) == 0
    assert isinstance(plan_output.task_resource_supply, TaskResourceSupplyOutput)
    assert isinstance(plan_output.resource_calendar_plan, ResourceCalendarPlanOutput)
    assert isinstance(plan_output.resource_utilization, ResourceUtilizationOutput)
    assert len(plan_output.resource_lacks) == 0

def test_task_resource_supply_output_holds_data():
    task_resource_supply = TaskResourceSupplyOutput()

    assert len(task_resource_supply.rows) == 0


def test_task_resource_row_supply_output_holds_data():
    task_resource_supply_row = TaskResourceSupplyRowOutput(
        task_id='CR-1',
        task_name='Change Request 1',
        business_line='BL-1',
        is_fully_supplied=True,
        is_fully_supplied_highlight=HighlightOutput.REGULAR
    )

    assert task_resource_supply_row.task_id == 'CR-1'
    assert task_resource_supply_row.task_name == 'Change Request 1'
    assert task_resource_supply_row.business_line == 'BL-1'
    assert task_resource_supply_row.is_fully_supplied == True
    assert task_resource_supply_row.is_fully_supplied_highlight == HighlightOutput.REGULAR
    assert len(task_resource_supply_row.skill_resource_supply) == 0


def test_skill_resource_supply_holds_data():
    skill_resource_supply = SkillResourceSupplyOutput(
        system='SYS-1',
        ability=AbilityEnum.SYSTEM_ANALYSIS,
        supply_percent=1.0,
        highlight=HighlightOutput.REGULAR
    )

    assert skill_resource_supply.system == 'SYS-1'
    assert skill_resource_supply.ability == AbilityEnum.SYSTEM_ANALYSIS
    assert skill_resource_supply.supply_percent == 1.0

def test_resource_calendar_plan_holds_attributes():
    resource_calendar_plan = ResourceCalendarPlanOutput()
    assert len(resource_calendar_plan.tasks) == 0

def test_bottleneck_hint_holds_attributes():
    bottleneck_hint = ResourceCalendarPlanBottleneckHintOutput(
        task_id='T-1',
        system='SYS-1',
        ability=AbilityEnum.DEVELOPMENT
    )

    assert bottleneck_hint.task_id == 'T-1'
    assert bottleneck_hint.system == 'SYS-1'
    assert bottleneck_hint.ability == AbilityEnum.DEVELOPMENT

def test_task_output_holds_attributes():
    task = ResourceCalendarPlanTaskOutput(
        id='CR-1',
        name='Change request 1',
        business_line='BL-1',
        start_date_or_empty_string=date(2020, 10, 5),
        start_date_highlight=HighlightOutput.REGULAR,
        end_date_or_empty_string=date(2020, 10, 10),
        end_date_highlight=HighlightOutput.REGULAR,
        initial_effort_hours=120.0,
        assigned_effort_hours=120.0,
        planned_readiness=1.0,
        planned_readiness_highlight=HighlightOutput.REGULAR
    )

    assert task.id == 'CR-1'
    assert task.name == 'Change request 1'
    assert task.business_line == 'BL-1'
    assert task.start_date_or_empty_string == date(2020, 10, 5)
    assert task.start_date_highlight == HighlightOutput.REGULAR
    assert task.end_date_or_empty_string == date(2020, 10, 10)
    assert task.end_date_highlight == HighlightOutput.REGULAR
    assert task.initial_effort_hours == 120
    assert task.assigned_effort_hours == 120
    assert task.planned_readiness == 1
    assert task.planned_readiness_highlight == HighlightOutput.REGULAR
    assert len(task.sub_tasks) == 0
    assert len(task.groups) == 0
    assert len(task.predecessor_ids) == 0
    assert len(task.bottleneck_hints) == 0

def test_group_output_holds_attributes():
    group = ResourceCalendarPlanGroupOutput(
        system='SYS-1',
        ability=AbilityEnum.DEVELOPMENT,
        initial_hours=100,
        planned_hours=80,
        planned_readiness=0.8,
        highlight=HighlightOutput.ERROR,
        is_bottleneck=True
    )

    assert group.system == 'SYS-1'
    assert group.ability == AbilityEnum.DEVELOPMENT
    assert group.initial_hours == 100
    assert group.planned_hours == 80
    assert group.planned_readiness == 0.8
    assert group.highlight == HighlightOutput.ERROR
    assert group.is_bottleneck
    assert len(group.members) == 0

def test_member_output_holds_attributes():
    group = ResourceCalendarPlanMemberOutput(
        resource_id='DEV-1',
        resource_name='Developer 1',
        highlight=HighlightOutput.ERROR,
        start_date_or_empty_string=date(2020, 10, 5),
        start_date_highlight=HighlightOutput.REGULAR,
        end_date_or_empty_string=date(2020, 10, 10),
        end_date_highlight=HighlightOutput.ERROR,
        effort_decrease_hours=1.0
    )

    assert group.resource_id == 'DEV-1'
    assert group.resource_name == 'Developer 1'
    assert group.highlight == HighlightOutput.ERROR
    assert group.start_date_or_empty_string == date(2020, 10, 5)
    assert group.start_date_highlight == HighlightOutput.REGULAR
    assert group.end_date_or_empty_string == date(2020, 10, 10)
    assert group.end_date_highlight == HighlightOutput.ERROR
    assert group.effort_decrease_hours == 1.0
    assert len(group.effort_decreases_by_date) == 0

def test_resource_utilization_holds_attributes():
    resource_utilization = ResourceUtilizationOutput()
    assert len(resource_utilization.resources) == 0

def test_resource_utilization_resource_holds_attributes():
    resource = ResourceUtilizationResourceOutput(id='DEV-1', name='Developer', business_line='BL-1')

    assert resource.id == 'DEV-1'
    assert resource.name == 'Developer'
    assert resource.business_line == 'BL-1'
    assert len(resource.tasks) == 0
    assert len(resource.utilization_by_date.values()) == 0

def test_resource_utilization_percent_holds_attributes():
    resource_utilization_percent = ResourceUtilizationPercentOutput(value=0.5, highlight=HighlightOutput.WARNING)

    assert resource_utilization_percent.value == 0.5
    assert resource_utilization_percent.highlight == HighlightOutput.WARNING

def test_resource_utilization_task_holds_attributes():
    resource_utilization_task = ResourceUtilizationTaskOutput(id='CR-1', name='Change Request 1')

    assert resource_utilization_task.id == 'CR-1'
    assert resource_utilization_task.name == 'Change Request 1'
    assert len(resource_utilization_task.hours_spent_by_day.values()) == 0

def test_task_output_holds_data():
    task = TaskOutput(id='CR-1', name='Change Request 1', system='SYS-1', business_line='BL-1')
    assert task.id == 'CR-1'
    assert task.name == 'Change Request 1'
    assert task.system == 'SYS-1'
    assert task.business_line == 'BL-1'
    assert len(task.efforts) == 0
    assert len(task.sub_tasks) == 0
    assert len(task.predecessors) == 0
    assert len(task.team_members) == 0


def test_task_output_raises_value_error_when_supplied_with_parameters_of_wrong_type():
    with pytest.raises(ValueError):
        _ = TaskOutput(id=math.nan, name='Change Request 1', system='SYS-1', business_line='BL-1')

    with pytest.raises(ValueError):
        _ = TaskOutput(id='CR-1', name=math.nan, system='SYS-1', business_line='BL-1')

    with pytest.raises(ValueError):
        _ = TaskOutput(id='CR-1', name='Change Request 1', system=math.nan, business_line='BL-1')

    with pytest.raises(ValueError):
        _ = TaskOutput(id='CR-1', name='Change Request 1', system='SYS-1', business_line=math.nan)

def test_effort_output_holds_data():
    ability_hours = EffortOutput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=7.0)

    assert ability_hours.ability == AbilityEnum.SYSTEM_ANALYSIS
    assert ability_hours.hours == 7

def test_team_member_output_holds_attributes():
    team_member = TeamMemberOutput(system='SYS-1', ability=AbilityEnum.DEVELOPMENT, resource_ids_and_or_quantities=['1', 'foo@bar.com'])

    assert team_member.system == 'SYS-1'
    assert team_member.ability == AbilityEnum.DEVELOPMENT
    assert team_member.resource_ids_and_or_quantities == ['1', 'foo@bar.com']

def test_team_member_output_raises_exception_if_supplied_with_parameters_of_wrong_type():
    with pytest.raises(ValueError):
        _ = TeamMemberOutput(
            system=math.nan,
            ability=AbilityEnum.DEVELOPMENT,
            resource_ids_and_or_quantities=['1', 'foo@bar.com']
        )

    with pytest.raises(ValueError):
        _ = TeamMemberOutput(
            system='SYS-1',
            ability=math.nan,
            resource_ids_and_or_quantities=['1', 'foo@bar.com']
        )

    with pytest.raises(ValueError):
        _ = TeamMemberOutput(
            system='SYS-1',
            ability=AbilityEnum.DEVELOPMENT,
            resource_ids_and_or_quantities=math.nan
        )

    with pytest.raises(ValueError):
        _ = TeamMemberOutput(
            system='SYS-1',
            ability=AbilityEnum.DEVELOPMENT,
            resource_ids_and_or_quantities=[math.nan]
        )

def test_resource_lack_output_holds_attributes():
    resource_lack = ResourceLackOutput(business_line='BL-1', system='SYS-1')

    assert resource_lack.business_line == 'BL-1'
    assert resource_lack.system == 'SYS-1'
    assert len(resource_lack.efforts) == 0




