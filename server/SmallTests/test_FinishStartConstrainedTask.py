import datetime
import pytest

from Entities.Assignment.AssignmentEntry import AssignmentEntry
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
from Entities.Task.FinishStartConstrainedTask import FinishStartConstrainedTask
from Entities.Task.SimpleTask import SimpleTask
from Entities.Team.ConcreteResourceMember import ConcreteResourceMember
from Entities.Team.Team import Team


def test_finish_start_constrained_task_holds_attributes():
    team = Team(business_line='BL-1')
    plain_task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=team)
    follower_task = FinishStartConstrainedTask(task=plain_task)
    assert len(follower_task.predecessors) == 0


def test_finish_start_constrained_task_is_not_assignable_if_predecessor_does_not_have_finish_date():
    predecessor_task_team = Team(business_line='BL-1')
    predecessor = SimpleTask(id='P-1', name='Predecessor Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=predecessor_task_team)

    plain_task_team = Team(business_line='BL-1')
    plain_task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=plain_task_team)
    follower_task = FinishStartConstrainedTask(task=plain_task)
    follower_task.predecessors = [predecessor]
    assert not follower_task.can_be_worked_on_date(date=datetime.date(2020, 10, 1))


def test_finish_start_constrained_task_is_assignable_if_all_predecessors_get_end_date():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 16)

    predecessor_1_team = Team(business_line='BL-1')
    predecessor_1 = SimpleTask(
        id='P-1',
        name='Predecessor Task-1',
        business_line='BL-1',
        efforts=Efforts(effort_entries=[Effort(
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            hours=7.0)]
        ),
        team=predecessor_1_team
    )

    predecessor_2_team = Team(business_line='BL-1')
    predecessor_2 = SimpleTask(
        id='P-2',
        name='Predecessor Task-2',
        business_line='BL-1',
        efforts=Efforts(effort_entries=[Effort(
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            hours=7.0)]
        ),
        team=predecessor_2_team
    )

    plain_task_team = Team(business_line='BL-1')
    plain_task = SimpleTask(
        id='T-1',
        name='Task-1',
        business_line='BL-1',
        efforts=Efforts(
            effort_entries=[Effort(
                skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
                hours=70.0)]
        ),
        team=plain_task_team
    )

    follower_task = FinishStartConstrainedTask(task=plain_task)
    follower_task.predecessors = [predecessor_1, predecessor_2]

    capacities = Capacities(
        work_hours_per_day=1000.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    member = ConcreteResourceMember(
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        concrete_resource=resource
    )

    planner = Plan(start_date=work_date_start, end_date=work_date_end)

    planner.simulate_member_worked_on_task_for_day(member=member, task=predecessor_1, date=datetime.date(2020, 10, 7))
    assert predecessor_1.has_end_date()
    assert predecessor_1.get_end_date() == datetime.date(2020, 10, 7)

    planner.simulate_member_worked_on_task_for_day(member=member, task=predecessor_2, date=datetime.date(2020, 10, 6))
    assert predecessor_2.has_end_date()
    assert predecessor_2.get_end_date() == datetime.date(2020, 10, 6)

    assert follower_task.are_all_predecessors_have_end_date()
    assert follower_task.get_predecessors_max_end_date() == datetime.date(2020, 10, 7)

    assert not follower_task.can_be_worked_on_date(date=datetime.date(2020, 10, 5))
    assert not follower_task.can_be_worked_on_date(date=datetime.date(2020, 10, 6))
    assert not follower_task.can_be_worked_on_date(date=datetime.date(2020, 10, 7))
    assert follower_task.can_be_worked_on_date(date=datetime.date(2020, 10, 8))

    with pytest.raises(ValueError):
        assignment = AssignmentEntry(
            task=follower_task,
            resource=resource,
            date=datetime.date(2020, 10, 5),
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            task_effort_decrease_hours=1,
            resource_spent_hours=1
        )
        follower_task.accept_assignment(
            assignment=assignment
        )


    assert follower_task.get_remaining_efforts_hours() == 70
    planner.simulate_member_worked_on_task_for_day(member=member, task=follower_task, date=datetime.date(2020, 10, 5))
    assert follower_task.get_remaining_efforts_hours() == 70
    planner.simulate_member_worked_on_task_for_day(member=member, task=follower_task, date=datetime.date(2020, 10, 6))
    assert follower_task.get_remaining_efforts_hours() == 70
    planner.simulate_member_worked_on_task_for_day(member=member, task=follower_task, date=datetime.date(2020, 10, 7))
    assert follower_task.get_remaining_efforts_hours() == 70


    planner.simulate_member_worked_on_task_for_day(member=member, task=follower_task, date=datetime.date(2020, 10, 8))
    assert follower_task.get_remaining_efforts_hours() == 0

def test_finish_start_constrained_task_with_zero_effort_returns_it_s_predecessors_end_date():
    work_date_start = datetime.date(2020, 10, 3)
    work_date_end = datetime.date(2020, 10, 16)

    predecessor_1_team = Team(business_line='BL-1')
    predecessor_1 = SimpleTask(
        id='P-1',
        name='Predecessor Task-1',
        business_line='BL-1',
        efforts=Efforts(effort_entries=[Effort(
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            hours=7.0)]
        ),
        team=predecessor_1_team
    )

    predecessor_2_team = Team(business_line='BL-1')
    predecessor_2 = SimpleTask(
        id='P-2',
        name='Predecessor Task-2',
        business_line='BL-1',
        efforts=Efforts(effort_entries=[Effort(
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            hours=7.0)]
        ),
        team=predecessor_2_team
    )

    plain_task_team = Team(business_line='BL-1')
    plain_task_with_zero_effort = SimpleTask(
        id='T-1',
        name='Task-1',
        business_line='BL-1',
        efforts=Efforts(
            effort_entries=[]
        ),
        team=plain_task_team
    )

    follower_task_with_zero_effort = FinishStartConstrainedTask(task=plain_task_with_zero_effort)
    follower_task_with_zero_effort.predecessors = [predecessor_1, predecessor_2]

    capacities = Capacities(
        work_hours_per_day=1000.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(
        id='foo@bar.com',
        name='Foo',
        work_date_start=work_date_start,
        work_date_end=work_date_end,
        business_line='BL-1',
        capacities=capacities
    )

    member = ConcreteResourceMember(
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        concrete_resource=resource
    )

    planner = Plan(start_date=work_date_start, end_date=work_date_end)

    planner.simulate_member_worked_on_task_for_day(member=member, task=predecessor_1, date=datetime.date(2020, 10, 7))
    assert predecessor_1.has_end_date()
    assert predecessor_1.get_end_date() == datetime.date(2020, 10, 7)

    planner.simulate_member_worked_on_task_for_day(member=member, task=predecessor_2, date=datetime.date(2020, 10, 6))
    assert predecessor_2.has_end_date()
    assert predecessor_2.get_end_date() == datetime.date(2020, 10, 6)

    assert follower_task_with_zero_effort.has_start_date()
    assert follower_task_with_zero_effort.get_start_date() == datetime.date(2020, 10, 7)

    assert follower_task_with_zero_effort.has_end_date()
    assert follower_task_with_zero_effort.get_end_date() == datetime.date(2020, 10, 7)
