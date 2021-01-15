from datetime import date
import pytest
from Entities.Plan.Plan import Plan
from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Resource.Calendar.VacationCalendar import VacationCalendar
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
from Entities.Team.InconcreteResourceMember import InconcreteResourceMember
from Entities.Team.Team import Team


def test_plan_holds_attributes():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    assert plan.start_date == work_date_start
    assert plan.end_date == work_date_end
    assert len(plan.tasks) == 0
    assert len(plan.resources) == 0
    assert len(plan.teams) == 0

def test_plan_work_on_task_for_day_ignoring_children_generates_assignment_and_get_task_returns_distinct_tasks():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=0.5)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(
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
        concrete_resource=resource
    )

    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=14.0)])
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    plan.simulate_member_worked_on_task_for_day_ignoring_sub_tasks(member=member, task=task, date=date(2020, 10, 5))
    plan.simulate_member_worked_on_task_for_day_ignoring_sub_tasks(member=member, task=task, date=date(2020, 10, 6))

    assert resource.get_remaining_work_hours() == 0
    assert task.get_remaining_efforts_hours() == 7
    assert len(resource.assignments.assignment_list) == 2
    resource_assignment_0 = resource.assignments.assignment_list[0]
    assert resource_assignment_0.resource == resource
    assert resource_assignment_0.task == task
    assert resource_assignment_0.date == date(2020, 10, 5)
    assert resource_assignment_0.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert resource_assignment_0.resource_spent_hours == 7
    assert resource_assignment_0.task_effort_decrease_hours == 3.5

    resource_assignment_1 = resource.assignments.assignment_list[1]
    assert resource_assignment_1.resource == resource
    assert resource_assignment_1.task == task
    assert resource_assignment_1.date == date(2020, 10, 6)
    assert resource_assignment_1.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert resource_assignment_1.resource_spent_hours == 7
    assert resource_assignment_1.task_effort_decrease_hours == 3.5

    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 5)) == 0

    assert resource.has_start_date()
    assert resource.get_start_date() == date(2020, 10, 5)
    assert resource.has_end_date()
    assert resource.get_end_date() == date(2020, 10, 6)

    assert len(task.get_assignments().assignment_list) == 2
    task_assignment_0 = task.get_assignments().assignment_list[0]
    assert task_assignment_0.resource == resource
    assert task_assignment_0.task == task
    assert task_assignment_0.date == date(2020, 10, 5)
    assert task_assignment_0.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert task_assignment_0.resource_spent_hours == 7
    assert task_assignment_0.task_effort_decrease_hours == 3.5

    task_assignment_1 = task.get_assignments().assignment_list[1]
    assert task_assignment_1.resource == resource
    assert task_assignment_1.task == task
    assert task_assignment_1.date == date(2020, 10, 6)
    assert task_assignment_1.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert task_assignment_1.resource_spent_hours == 7
    assert task_assignment_1.task_effort_decrease_hours == 3.5

    assert task.get_remaining_efforts_hours() == 7
    assert task.has_start_date()
    assert task.get_start_date() == date(2020, 10, 5)
    assert not task.has_end_date()
    with pytest.raises(ValueError):
        task.get_end_date()

    assert len(resource.get_tasks()) == 1

def test_plan_simulate_member_worked_on_task_for_day_generates_assignment():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 6)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=0.5)
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
    sub_task_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=7.0)])

    sub_task_team = Team(business_line='BL-1')
    sub_task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=sub_task_efforts, team=sub_task_team)
    task.set_direct_sub_tasks(sub_tasks=[sub_task])

    plan = Plan(start_date=work_date_start, end_date=work_date_end)
    plan.simulate_member_worked_on_task_for_day(member=member, task=task, date=date(2020, 10, 5))
    plan.simulate_member_worked_on_task_for_day(member=member, task=task, date=date(2020, 10, 6))

    assert len(resource.assignments.assignment_list) == 2
    resource_assignment_0 = resource.assignments.assignment_list[0]
    assert resource_assignment_0.resource == resource
    assert resource_assignment_0.task == sub_task
    assert resource_assignment_0.date == date(2020, 10, 5)
    assert resource_assignment_0.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert resource_assignment_0.resource_spent_hours == 7
    assert resource_assignment_0.task_effort_decrease_hours == 3.5

    resource_assignment_1 = resource.assignments.assignment_list[1]
    assert resource_assignment_1.resource == resource
    assert resource_assignment_1.task == sub_task
    assert resource_assignment_1.date == date(2020, 10, 6)
    assert resource_assignment_1.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert resource_assignment_1.resource_spent_hours == 7
    assert resource_assignment_1.task_effort_decrease_hours == 3.5

    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 5)) == 0

    assert resource.has_start_date()
    assert resource.get_start_date() == date(2020, 10, 5)
    assert resource.has_end_date()
    assert resource.get_end_date() == date(2020, 10, 6)

    assert len(sub_task.get_assignments().assignment_list) == 2
    sub_task_assignment_0 = sub_task.get_assignments().assignment_list[0]
    assert sub_task_assignment_0.resource == resource
    assert sub_task_assignment_0.task == sub_task
    assert sub_task_assignment_0.date == date(2020, 10, 5)
    assert sub_task_assignment_0.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert sub_task_assignment_0.resource_spent_hours == 7
    assert sub_task_assignment_0.task_effort_decrease_hours == 3.5

    sub_task_assignment_1 = sub_task.get_assignments().assignment_list[1]
    assert sub_task_assignment_1.resource == resource
    assert sub_task_assignment_1.task == sub_task
    assert sub_task_assignment_1.date == date(2020, 10, 6)
    assert sub_task_assignment_1.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert sub_task_assignment_1.resource_spent_hours == 7
    assert sub_task_assignment_1.task_effort_decrease_hours == 3.5

    assert sub_task.has_start_date()
    assert sub_task.get_start_date() == date(2020, 10, 5)
    assert sub_task.has_end_date()
    assert sub_task.get_end_date() == date(2020, 10, 6)

    assert task.has_start_date()
    assert task.get_start_date() == date(2020, 10, 5)
    assert task.has_end_date()
    assert task.get_end_date() == date(2020, 10, 6)

    assert sub_task.get_remaining_efforts_hours() == 0

def test_plan_simulate_member_worked_on_task_decreases_task_effort_if_has_suitable_skill():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 16)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    team = Team(business_line='BL-1')
    member = ConcreteResourceMember(
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        concrete_resource=resource
    )

    efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    plan.simulate_member_worked_on_task(member=member, task=task)

    assert task.get_remaining_efforts_hours() == 30


def test_plan_simulate_inconcrete_member_worked_on_task_in_multiple_roles_decreases_task_effort_if_has_suitable_skill():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 7)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacities.capacity_list = [
        CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS), efficiency=1.0),
        CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_TESTING), efficiency=1.0)
    ]

    resource = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    assert resource.get_remaining_work_hours() == 21

    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 3)) == 0
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 4)) == 0
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 5)) == 7
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 6)) == 7
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 7)) == 7

    team = Team(business_line='BL-1')
    member_with_skill_1 = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS)
    )
    team.add_member(member=member_with_skill_1)

    member_with_skill_2 = InconcreteResourceMember(
        business_line='BL-1',
        skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_TESTING),
    )
    team.add_member(member=member_with_skill_2)
    team.resource_pool = [resource]

    efforts = Efforts(
        effort_entries=[
            Effort(skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS), hours=10.0),
            Effort(skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_TESTING), hours=10.0)
        ])
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)
    plan.tasks = [task]
    plan.resources = [resource]
    plan.teams = [team]

    plan.plan_leveled()

    assert task.get_remaining_efforts_hours() == 0

    assert resource.get_remaining_work_hours() == 1

    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 5)) == 0
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 6)) == 0
    assert resource.get_remaining_work_hours_for_date(date=date(2020, 10, 7)) == 1

    assert resource.get_hours_spent_for_task_and_date_and_skill(task=task, date=date(2020, 10, 5), skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS)) == 6
    assert resource.get_hours_spent_for_task_and_date_and_skill(task=task, date=date(2020, 10, 6), skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS)) == 3
    assert resource.get_hours_spent_for_task_and_date_and_skill(task=task, date=date(2020, 10, 7), skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_ANALYSIS)) == 1

    assert resource.get_hours_spent_for_task_and_date_and_skill(task=task, date=date(2020, 10, 5), skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_TESTING)) == 1
    assert resource.get_hours_spent_for_task_and_date_and_skill(task=task, date=date(2020, 10, 6), skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_TESTING)) == 4
    assert resource.get_hours_spent_for_task_and_date_and_skill(task=task, date=date(2020, 10, 7), skill=Skill(system='Foo', ability=AbilityEnum.SYSTEM_TESTING)) == 5

def test_plan_simulate_member_worked_on_task_decreases_remaining_work_hours_if_has_suitable_skill_and_sets_start_and_end_date():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 16)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

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

    sub_task_team = Team(business_line='BL-1')
    sub_task_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)])
    sub_task = SimpleTask(id='ST-1', name='Subtask-1', business_line='BL-1', efforts=sub_task_efforts, team=sub_task_team)
    task.set_direct_sub_tasks(sub_tasks=[sub_task])

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    plan.simulate_member_worked_on_task(member=member, task=task)

    assert resource.get_remaining_work_hours() == 60
    assert resource.has_start_date()
    assert resource.get_start_date() == date(2020, 10, 5)
    assert resource.has_end_date()
    assert resource.get_end_date() == date(2020, 10, 6)

def test_plan_simulate_member_worked_on_task_does_not_decrease_task_effort_if_different_business_line():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 16)

    capacities = Capacities(work_hours_per_day=8.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

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

    assert resource.get_remaining_work_hours() == 80

    task_team = Team(business_line='BL-1')
    task_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])
    task = SimpleTask(id='T-1', name='Task-1', business_line='Different Business Line', efforts=task_efforts, team=task_team)

    sub_task_team =  Team(business_line='BL-1')
    sub_task_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])
    sub_task = SimpleTask(id='ST-1', name='Subtask-1', business_line='Different Business Line', efforts=sub_task_efforts, team=sub_task_team)

    task.set_direct_sub_tasks(sub_tasks=[sub_task])

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    plan.simulate_member_worked_on_task(member=member, task=task)

    assert task.get_remaining_efforts_hours() == 200
    assert resource.get_remaining_work_hours() == 80


def test_plan_simulate_member_worked_on_task_does_not_decrease_task_effort_if_does_not_have_suitable_skill():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 3 + 14)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

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

    sub_task_team = Team(business_line='BL-1')
    sub_task_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])
    sub_task = SimpleTask(id='ST-1', name='Subtask-1', business_line='BL-1', efforts=sub_task_efforts, team=sub_task_team)
    task.set_direct_sub_tasks(sub_tasks=[sub_task])

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    plan.simulate_member_worked_on_task(member=member, task=task)

    assert task.get_remaining_efforts_hours() == 100


def test_plan_simulate_member_worked_on_task_is_not_helpful_when_no_work_hours_left():
    work_date_start = date(2020, 10, 5)
    work_date_end = date(2020, 10, 5)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

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

    sub_task_team = Team(business_line='BL-1')
    sub_task_efforts = Efforts(
        effort_entries=[Effort(skill=Skill(system='Bar', ability=AbilityEnum.DEVELOPMENT), hours=100.0)])
    sub_task = SimpleTask(id='ST-1', name='Subtask-1', business_line='BL-1', efforts=sub_task_efforts, team=sub_task_team)
    task.set_direct_sub_tasks(sub_tasks=[sub_task])

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    plan.simulate_member_worked_on_task(member=member, task=task)

    assert resource.get_remaining_work_hours() == 7
    assert not resource.is_helpful_in_performing_task_for_date(task=task, date=date(2020, 10, 3))

def test_plan_levels_resource_3_5_hours_in_3_days_to_1_75_hours_for_6_days():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 13)

    plan = Plan(start_date=work_date_start, end_date=work_date_end)

    capacities = Capacities(
        work_hours_per_day=7.0,
        calendar=VacationCalendar(holidays=[date(2020, 10, 13)], working_days=[], child_calendar=RussianCalendar()),
        efficiency_in_time=ConstantEfficiency()
    )

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=0.5)
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

    efforts = Efforts(effort_entries=[Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=1.75 * 6)])

    team = Team(business_line='BL-1')
    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    plan.simulate_member_worked_on_task(member=member, task=task)

    assert task.get_remaining_efforts_hours() == 0
    assert sum([assignment.task_effort_decrease_hours for assignment in
                resource.assignments.get_assignment_entries_for_task_and_skill(task=task, resource=resource,
                                                                               skill=Skill(system='Foo',
                                                                                           ability=AbilityEnum.DEVELOPMENT))]) == 1.75 * 6

    assert sum([assignment['total_resource_spendable_hours'] for assignment in
        plan.get_member_spendable_hours_for_task_and_period(
            member=member,
            task=task,
            start_date=work_date_start,
            end_date=work_date_end
        )]) == 7 * 6

    plan.level_member_effort_on_task_for_period(
        task=task,
        member=member,
        start_date=work_date_start,
        end_date=work_date_end
    )

    first_working_day_after_holiday_starting_2020_10_3 = date(2020, 10, 5)
    last_working_day_of_resource_before_vacation_starting_2020_10_13 = date(2020, 10, 12)
    assert task.get_start_date() == first_working_day_after_holiday_starting_2020_10_3
    assert task.get_end_date() == last_working_day_of_resource_before_vacation_starting_2020_10_13
    assert task.get_remaining_efforts_hours() == 0
    task_assignment_entries = task.get_assignment_entries_for_resource(resource=resource)
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 3)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 4)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 5)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 6)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 7)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 8)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 9)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 10)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 11)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 12)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 13)]) == 0

    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 3)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 4)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 5)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 6)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 7)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 8)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 9)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 10)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 11)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 12)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_assignment_entries if
                assignment_entry.date == date(2020, 10, 13)]) == 0


    resource_assignment_entries = resource.assignments.assignment_list
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 3)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 4)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 5)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 6)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 7)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 8)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 9)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 10)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 11)]) == 0
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 12)]) == 3.5
    assert sum([assignment_entry.resource_spent_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 13)]) == 0

    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 3)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 4)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 5)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 6)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 7)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 8)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 9)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 10)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 11)]) == 0
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 12)]) == 1.75
    assert sum([assignment_entry.task_effort_decrease_hours for assignment_entry in resource_assignment_entries if
                assignment_entry.date == date(2020, 10, 13)]) == 0




