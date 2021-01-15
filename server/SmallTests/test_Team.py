import datetime

import pytest

from Entities.Plan.Plan import Plan
from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Resource.Capacity.Capacities import Capacities
from Entities.Resource.Capacity.CapacityEntry import CapacityEntry
from Entities.Resource.EfficiencyInTime.ConstantEfficiency import ConstantEfficiency
from Entities.Resource.SimpleResource import SimpleResource
from Entities.Skill.AbilityEnum import AbilityEnum
from Entities.Skill.Skill import Skill
from Entities.Task.Effort.Effort import Effort
from Entities.Task.Effort.Efforts import Efforts
from Entities.Task.SimpleTask import SimpleTask
from Entities.Team.ConcreteResourceMember import ConcreteResourceMember
from Entities.Team.GroupOfMembersHavingSameSkill import GroupOfMembersHavingSameSkill
from Entities.Team.InconcreteResourceMember import InconcreteResourceMember
from Entities.Team.Team import Team


def test_team_holds_attributes():
    team = Team(business_line='BL-1')

    assert team.business_line == 'BL-1'
    assert len(team.groups) == 0
    assert len(team.resource_pool) == 0

def test_group_holds_attributes():
    group = GroupOfMembersHavingSameSkill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))

    assert group.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert len(group.members) == 0
    assert not group.is_bottleneck

def test_concrete_resource_member_holds_attributes():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 12)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    member = ConcreteResourceMember(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), concrete_resource=resource)

    assert member.get_skill() == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert member.concrete_resource == resource
    assert member.get_picked_resource() == resource

def test_inconcrete_resource_member_hold_attributes():
    member = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))

    assert member.get_skill() == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert member.business_line == 'BL-1'
    assert member.get_skill() == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)

def test_when_team_adds_member_then_has_group_for_skill_returns_true_if_has_skill_and_false_otherwise():
    team = Team(business_line='BL-1')
    member_1 = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))
    team.add_member(member=member_1)
    member_2 = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_ANALYSIS))
    team.add_member(member=member_2)

    assert team.has_group_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))
    assert team.has_group_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_ANALYSIS))
    assert not team.has_group_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS))
    assert not team.has_group_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT))

def test_when_team_adds_member_then_get_group_for_skill_returns_group_if_has_skill_and_raises_value_error_otherwise():
    team = Team(business_line='BL-1')
    member_1 = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))
    team.add_member(member=member_1)
    member_2 = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_ANALYSIS))
    team.add_member(member=member_2)

    assert team.get_group_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)).skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert team.get_group_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_ANALYSIS)).skill == Skill(system='Bar', ability=AbilityEnum.SYSTEM_ANALYSIS)
    with pytest.raises(ValueError):
        team.get_group_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS))
    with pytest.raises(ValueError):
        team.get_group_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT))

def test_when_team_adds_member_with_same_skill_twice_only_one_group_created():
    team = Team(business_line='BL-1')
    member_1 = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))
    team.add_member(member=member_1)
    member_2 = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))
    team.add_member(member=member_2)

    assert len(team.groups) == 1

def test_inconcrete_resource_member_picks_resources_picks_resources_from_same_business_line_and_skill():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 12)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1)
    capacities.capacity_list = [capacity_entry]

    resource_to_pick = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    member = InconcreteResourceMember(business_line='BL-1', skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))

    team = Team(business_line='BL-1')
    team.add_member(member=member)

    efforts = Efforts(effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=28)])

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    member.pick_resource_for_task(task=task, start_date=work_date_start, end_date=work_date_end, resource_pool=[resource_to_pick])

    assert member.has_picked_resource()
    assert member.get_picked_resource() == resource_to_pick

def test_plan_will_not_use_resource_not_from_a_team_even_it_exists_in_resources():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 12)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1)
    capacities.capacity_list = [capacity_entry]

    resource_in_team = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    resource_not_in_team = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    team = Team(business_line='BL-1')

    member = ConcreteResourceMember(
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        concrete_resource=resource_in_team
    )
    team.add_member(member=member)
    team.resource_pool = [resource_in_team, resource_not_in_team]
    plan.teams = [team]

    efforts = Efforts(effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=28)])

    task_that_can_be_finished_in_four_days = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan.tasks = [task_that_can_be_finished_in_four_days]
    plan.resources = [resource_in_team, resource_not_in_team]

    plan.plan_leveled()

    first_friday = datetime.date(2020, 10, 8)
    assert task_that_can_be_finished_in_four_days.get_end_date() == first_friday

def test_team_will_not_pick_same_resource_twice():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 12)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1)
    capacities.capacity_list = [capacity_entry]

    resource_1 = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    resource_2 = SimpleResource(
        id='bar@bar.com',
        name='Bar',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    efforts = Efforts(effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=28)])

    team = Team(business_line='BL-1')

    member_1 = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    )
    team.add_member(member=member_1)

    member_2 = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    )
    team.add_member(member=member_2)

    team.resource_pool = [resource_1, resource_2]

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    team.pick_resources_for_task(task=task, start_date=work_date_start, end_date=work_date_end)

    assert len(team.groups) == 1
    assert len(team.groups[0].members) == 2
    assert member_1.get_picked_resource() != member_2.get_picked_resource()

def test_planner_marks_group_as_bottleneck_if_effort_hours_with_same_skill_left_after_planning():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 12)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)


    team = Team(business_line='BL-1')

    member_without_resource = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    )
    team.add_member(member=member_without_resource)

    efforts = Efforts(effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=28)])

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan.tasks = [task]

    plan.teams = [team]

    plan.plan_leveled()

    assert team.groups[0].is_bottleneck

def test_planner_marks_group_as_bottleneck_if_no_effort_hours_left_after_planning_and_group_has_largest_last_assignment_date_among_other_groups_in_team():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 12)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1)
    capacities.capacity_list = [capacity_entry]

    resource_1 = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    resource_2 = SimpleResource(
        id='bar@bar.com',
        name='Bar',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    efforts = Efforts(effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=28)])

    team = Team(business_line='BL-1')

    member_1 = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    )
    team.add_member(member=member_1)

    member_2 = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    )
    team.add_member(member=member_2)

    team.resource_pool = [resource_1, resource_2]

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan.tasks = [task]

    plan.teams = [team]

    plan.plan_leveled()

    assert team.groups[0].is_bottleneck