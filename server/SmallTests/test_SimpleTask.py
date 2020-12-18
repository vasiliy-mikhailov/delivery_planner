from datetime import date
import pytest
from Entities.Assignment.AssignmentEntry import AssignmentEntry
from Entities.Assignment.Assignments import Assignments
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
from Entities.Team.Team import Team


def test_simple_task_holds_attributes():
    efforts = Efforts(
        effort_entries=[Effort(
            skill=Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE),
            hours=1.0)]
    )

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    assert task.get_id() == 'T-1'
    assert len(task.get_direct_sub_tasks()) == 0
    assert task.get_business_line() == 'BL-1'
    assert task.get_remaining_efforts_hours() == 1
    assert task.get_initial_efforts_hours() == 1
    assert task.get_initial_efforts_ignoring_sub_tasks().get_hours() == 1
    assert task.get_team() == team
    assert isinstance(task.get_assignments(), Assignments)

    assert not task.has_start_date()
    with pytest.raises(ValueError):
        task.get_start_date()

    assert not task.has_end_date()
    with pytest.raises(ValueError):
        task.get_end_date()


def test_task_plan_resource_for_day_decreases_effort_and_creates_assignment():
    team = Team(business_line='BL-1')

    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 16)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=0.5)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    assignment = AssignmentEntry(
        task=task,
        resource=resource,
        date=date(2020, 10, 5),
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    task.accept_assignment(assignment)

    assert task.get_remaining_efforts_hours() == 96.5
    assert len(task.get_assignments().assignment_list) == 1
    assignment_0: AssignmentEntry = task.get_assignments().assignment_list[0]
    assert assignment_0.resource == resource
    assert assignment_0.task == task
    assert assignment_0.date == date(2020, 10, 5)
    assert assignment_0.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert assignment_0.task_effort_decrease_hours == 3.5
    assert assignment_0.resource_spent_hours == 7
    assert len(task.get_assignment_entries_for_resource(resource)) == 1


def test_simple_task_calculates_own_remaining_efforts_and_child_remaining_efforts():
    task_team = Team(business_line='BL-1')
    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE), hours=10.0)])
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=task_team)

    sub_task_1_team = Team(business_line='BL-1')
    efforts_1 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)])
    sub_task1 = SimpleTask(id='ST-1', name='Subtask-1', business_line='BL-1', efforts=efforts_1, team=sub_task_1_team)

    sub_task_2_team = Team(business_line='BL-1')
    efforts_2 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT), hours=10.0)])
    sub_task2 = SimpleTask(id='ST-2', name='Subtask-2', business_line='BL-1', efforts=efforts_2, team=sub_task_2_team)

    sub_task_3_team = Team(business_line='BL-1')
    efforts_3 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT), hours=10.0)])
    sub_task3 = SimpleTask(id='ST-3', name='Subtask-3', business_line='BL-1', efforts=efforts_3, team=sub_task_3_team)

    task.set_direct_sub_tasks(sub_tasks=[sub_task1, sub_task2, sub_task3])

    assert task.get_remaining_efforts_hours_ignoring_sub_tasks() == 10
    assert task.get_remaining_efforts_hours_for_sub_tasks() == 30
    assert task.get_remaining_efforts_hours() == 40
    assert task.get_remaining_efforts_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE)) == 10
    assert task.get_remaining_efforts_hours_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)) == 10
    assert task.get_remaining_efforts_hours_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT)) == 20

    initial_efforts = task.get_initial_efforts()
    assert initial_efforts.get_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE)) == 10
    assert initial_efforts.get_hours_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)) == 10
    assert initial_efforts.get_hours_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT)) == 20


def test_simple_task_can_be_worked_on_returns_true_for_any_day():
    team = Team(business_line='BL-1')

    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE), hours=1.0)])
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    assert task.can_be_worked_on_date(date=date(2020, 10, 1))


def test_working_on_subtasks_sets_task_start_and_end_date():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 6)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    member = ConcreteResourceMember(
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        concrete_resource=resource
    )

    task_team = Team(business_line='BL-1')
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=task_team)

    sub_task_1_team = Team(business_line='BL-1')
    sub_task_efforts_1 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=7)])
    sub_task_1 = SimpleTask(id='ST-1', name='Subtask-1', business_line='BL-1', efforts=sub_task_efforts_1, team=sub_task_1_team)

    sub_task_2_team = Team(business_line='BL-1')
    sub_task_efforts_2 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=7)])
    sub_task_2 = SimpleTask(id='ST-2', name='Subtask-2', business_line='BL-1', efforts=sub_task_efforts_2, team=sub_task_2_team)

    task.set_direct_sub_tasks(sub_tasks=[sub_task_1, sub_task_2])

    planner = Plan(start_date=work_date_start, end_date=work_date_end)

    assert not task.has_start_date()
    with pytest.raises(ValueError):
        task.get_start_date()
    assert not task.has_end_date()
    with pytest.raises(ValueError):
        task.get_end_date()

    planner.simulate_member_worked_on_task(member=member, task=sub_task_1)
    planner.simulate_member_worked_on_task(member=member, task=sub_task_2)

    assert sub_task_1.has_start_date()
    assert sub_task_1.has_end_date()
    assert sub_task_2.has_start_date()
    assert sub_task_2.has_end_date()
    assert task.has_start_date()
    assert task.get_start_date() == date(2020, 10, 5)
    assert task.has_end_date()
    assert task.get_end_date() == date(2020, 10, 6)

def test_task_will_not_have_start_date_or_end_date_if_child_task_does_not_have_start_date_and_end_date():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 16)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=RussianCalendar(),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                              work_date_end=work_date_end,
                              business_line='BL-1',
                              capacities=capacities)

    task_team = Team(business_line='BL-1')
    member = ConcreteResourceMember(
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        concrete_resource=resource
    )
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=task_team)

    sub_task_1_team = Team(business_line='BL-1')
    sub_task_efforts_1 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)])
    sub_task_1 = SimpleTask(id='ST-1', name='Subtask-1', business_line='BL-1', efforts=sub_task_efforts_1, team=sub_task_1_team)

    sub_task_2_team = Team(business_line='BL-1')
    sub_task_efforts_2 = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)])
    sub_task_2 = SimpleTask(id='ST-2', name='Subtask-2', business_line='BL-1', efforts=sub_task_efforts_2, team=sub_task_2_team)

    task.set_direct_sub_tasks(sub_tasks=[sub_task_1, sub_task_2])

    planner = Plan(start_date=work_date_start, end_date=work_date_end)

    assert not task.has_start_date()
    with pytest.raises(ValueError):
        task.get_start_date()
    assert not task.has_end_date()
    with pytest.raises(ValueError):
        task.get_end_date()

    planner.simulate_member_worked_on_task(member=member, task=sub_task_1)

    assert sub_task_1.has_start_date()
    assert sub_task_1.has_end_date()
    assert not sub_task_2.has_start_date()
    assert not sub_task_2.has_end_date()
    assert not task.has_start_date()
    assert not task.has_end_date()
