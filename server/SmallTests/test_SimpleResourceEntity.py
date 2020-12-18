from datetime import date
import pytest
from Entities.Assignment.AssignmentEntry import AssignmentEntry
from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Assignment.Assignments import Assignments
from Entities.Resource.Capacity.Capacities import Capacities
from Entities.Resource.Capacity.CapacityEntry import CapacityEntry
from Entities.Resource.EfficiencyInTime.ConstantEfficiency import ConstantEfficiency
from Entities.Resource.SimpleResource import SimpleResource
from Entities.Skill.AbilityEnum import AbilityEnum
from Entities.Skill.Skill import Skill
from Entities.Task.Effort.Effort import Effort
from Entities.Task.Effort.Efforts import Efforts
from Entities.Task.SimpleTask import SimpleTask
from Entities.Team.Team import Team


def test_simple_resource_holds_attributes():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())
    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end, business_line='BL-1',
                            capacities=capacities
                            )

    assert resource.id == 'foo@bar.com'
    assert resource.capacities == capacities
    assert resource.work_date_start == work_date_start
    assert resource.work_date_end == work_date_end
    assert resource.business_line == 'BL-1'
    assert isinstance(resource.assignments, Assignments)
    assert len(resource.remaining_work_hours_for_date.keys()) == 7
    assert len(resource.initial_work_hours_for_date.keys()) == 7

def test_simple_resource_returns_initial_and_remaining_work_hours():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())
    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end, business_line='BL-1',
                            capacities=capacities
                            )

    assert resource.get_remaining_work_hours() == 35
    assert resource.get_initial_work_hours() == 35
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 3)) == 0
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 5)) == 7
    assert resource.get_initial_work_hours_for_date(date=date(2020, 10, 3)) == 0
    assert resource.get_initial_work_hours_for_date(date=date(2020, 10, 5)) == 7

def test_simple_resource_returns_zero_remaining_work_hours_outside_work_start_and_work_end_and_on_holidays():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())
    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end, business_line='BL-1',
                            capacities=capacities
                            )

    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 1)) == 0
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 11, 4)) == 0

def test_simple_resource_is_helpful_for_task_returns_true_if_has_ability_with_same_system_and_business_line():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    same_system_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])

    team = Team(business_line='BL-1')
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=same_system_efforts, team=team)

    assert resource.is_helpful_in_performing_task_for_date(task=task, date=date(2020, 10, 5))


def test_simple_resource_is_helpful_for_task_returns_true_if_has_ability_with_same_system_and_business_line_not_specified():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    same_system_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])

    team = Team(business_line='BL-1')
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=same_system_efforts, team=team)

    assert resource.is_helpful_in_performing_task_for_date(task=task, date=date(2020, 10, 5))


def test_simple_resource_is_helpful_for_task_returns_false_if_has_ability_with_same_system_and_different_business_line():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    efforts = Efforts([Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])

    team = Team(business_line='BL-2')
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-2', efforts=efforts, team=team)

    assert not resource.is_helpful_in_performing_task_for_date(task=task, date=date(2020, 10, 5))


def test_simple_resource_is_helpful_for_task_returns_false_if_has_no_ability_with_same_system():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT), hours=7.0)])

    team = Team(business_line='BL-1')
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    assert not resource.is_helpful_in_performing_task_for_date(task=task, date=date(2020, 10, 5))

def test_simple_resource_calculates_remaining_work_hours():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 11)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    assert resource.get_remaining_work_hours() == 35

def test_simple_resource_get_start_date_raises_exception_if_has_no_assignments():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)
    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    with pytest.raises(ValueError):
        resource.get_start_date()


def test_simple_resource_has_start_date_returns_false_if_has_no_assignments():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)
    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    assert not resource.has_start_date()


def test_simple_resource_get_end_date_raises_exception_if_has_no_assignments():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)
    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    with pytest.raises(ValueError):
        resource.get_end_date()


def test_simple_resource_has_end_date_returns_false_if_has_no_assignments():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)
    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    assert not resource.has_end_date()

def test_simple_resource_plan_work_on_task_for_day_decreases_effort_and_creates_assignment():
    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 16)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

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

    resource.accept_assignment(assignment=assignment)

    assert resource.get_remaining_work_hours() == 63
    assert len(resource.assignments.assignment_list) == 1
    assignment_0: AssignmentEntry = resource.assignments.assignment_list[0]
    assert assignment_0.resource == resource
    assert assignment_0.task == task
    assert assignment_0.date == date(2020, 10, 5)
    assert assignment_0.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert assignment_0.task_effort_decrease_hours == 3.5
    assert assignment_0.resource_spent_hours == 7

def test_simple_resource_has_skill_returns_true_if_has_skill_and_false_otherwise():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 9)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())
    capacity_entry = CapacityEntry(Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]
    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end, business_line='BL-1',
                            capacities=capacities
                            )

    assert resource.has_skill(skill=Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE))
    assert not resource.has_skill(skill=Skill(system='Bar', ability=AbilityEnum.SOLUTION_ARCHITECTURE))
    assert not resource.has_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))