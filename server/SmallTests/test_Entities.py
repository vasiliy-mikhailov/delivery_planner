import pytest

from Entities.ExternalTask.ExternalTask import ExternalTask
from Entities.ExternalTask.ExternalTaskEffort import ExternalTaskEffort
from Entities.Resource.Calendar.Calendar import generate_date_range
from Entities.Resource.Calendar.VacationCalendar import VacationCalendar
from Entities.Assignment.AssignmentEntry import AssignmentEntry, quantize_resource_spent_hours
from Entities.Assignment.Assignments import Assignments
from Entities.Resource.Capacity.Capacities import Capacities
from Entities.Resource.EfficiencyInTime.ConstantEfficiency import ConstantEfficiency
from Entities.Resource.EfficiencyInTime.LinearGrowthEfficiency import LinearGrowthEfficiency
from Entities.Resource.EfficiencyInTime.TimeBoundedConstantEfficiency import TimeBoundedConstantEfficiency
from Entities.Skill.Skill import Skill
from Entities.Task.Effort.Efforts import Efforts
from Entities.Task.SimpleTask import SimpleTask
from Entities.Task.Effort.Effort import Effort
from Entities.Skill.AbilityEnum import AbilityEnum
from Entities.Resource.SimpleResource import SimpleResource
from Entities.Resource.Capacity.CapacityEntry import CapacityEntry
from datetime import date
from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Resource.Calendar.BelarusCalendar import BelarusCalendar
from Entities.Team.Team import Team


def test_effort_entry_holds_attributes():
    effort_entry = Effort(Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE), hours=1.0)

    assert effort_entry.skill == Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE)
    assert effort_entry.hours == 1.0


def test_russian_calendar_returns_regular_workday_as_workday():
    calendar = RussianCalendar()
    test_date = date(2020, 10, 2)
    assert calendar.is_working_day(test_date)


def test_russian_calendar_returns_regular_weekend_as_not_workday():
    calendar = RussianCalendar()
    test_date = date(2020, 10, 3)
    assert not calendar.is_working_day(test_date)


def test_russian_calendar_returns_regular_holiday_as_not_workday():
    calendar = RussianCalendar()
    test_date = date(2020, 11, 4)
    assert not calendar.is_working_day(test_date)


def test_russian_calendar_returns_working_weekend_as_workday():
    calendar = RussianCalendar()
    test_date = date(2021, 2, 20)
    assert calendar.is_working_day(test_date)


def test_russian_calendar_has_247_working_days_in_2021():
    work_date_start = date(2021, 1, 1)
    work_date_end = date(2021, 12, 31)
    calendar = RussianCalendar()
    assert sum([calendar.is_working_day(day=day) for day in
                generate_date_range(start_date=work_date_start, end_date=work_date_end)]) == 247


def test_belarus_calendar_has_258_working_days_in_2021():
    work_date_start = date(2021, 1, 1)
    work_date_end = date(2021, 12, 31)
    calendar = BelarusCalendar()
    assert sum([calendar.is_working_day(day=day) for day in
                generate_date_range(start_date=work_date_start, end_date=work_date_end)]) == 258


def test_efforts_calculates_remaining_effort_hours():
    effort_entry_1 = Effort(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE), hours=10.0)
    effort_entry_2 = Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)
    effort_entry_3 = Effort(skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_TESTING), hours=10.0)

    efforts = Efforts(effort_entries=[effort_entry_1, effort_entry_2, effort_entry_3])
    assert efforts.get_hours() == 30
    assert efforts.get_hours_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)) == 10

def test_efforts_returns_skills():
    effort_entry_1 = Effort(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE), hours=10.0)
    effort_entry_2 = Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)
    effort_entry_3 = Effort(skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_TESTING), hours=10.0)

    efforts = Efforts(effort_entries=[effort_entry_1, effort_entry_2, effort_entry_3])
    skills = efforts.get_skills()

    assert len(skills) == 3
    assert Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE) in skills
    assert Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT) in skills
    assert Skill(system='Bar', ability=AbilityEnum.SYSTEM_TESTING) in skills

def test_efforts_adds_another_efforts():
    effort_entry_1_1 = Effort(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE), hours=10.0)
    effort_entry_1_2 = Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)
    effort_entry_1_3 = Effort(skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_TESTING), hours=10.0)
    efforts_1 = Efforts(effort_entries=[effort_entry_1_1, effort_entry_1_2, effort_entry_1_3])

    effort_entry_2_1 = Effort(skill=Skill(system='', ability=AbilityEnum.PROJECT_MANAGEMENT), hours=10.0)
    effort_entry_2_2 = Effort(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), hours=10.0)
    effort_entry_2_3 = Effort(skill=Skill(system='Buz', ability=AbilityEnum.SYSTEM_TESTING), hours=10.0)
    efforts_2 = Efforts(effort_entries=[effort_entry_2_1, effort_entry_2_2, effort_entry_2_3])

    efforts = efforts_1 + efforts_2
    assert efforts.get_hours() == 60
    assert efforts.get_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.SOLUTION_ARCHITECTURE)) == 10
    assert efforts.get_hours_for_skill(skill=Skill(system='', ability=AbilityEnum.PROJECT_MANAGEMENT)) == 10
    assert efforts.get_hours_for_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)) == 20
    assert efforts.get_hours_for_skill(skill=Skill(system='Bar', ability=AbilityEnum.SYSTEM_TESTING)) == 10
    assert efforts.get_hours_for_skill(skill=Skill(system='Buz', ability=AbilityEnum.SYSTEM_TESTING)) == 10


def test_constant_efficiency_returns_1_on_any_day():
    constant_efficiency = ConstantEfficiency()

    assert constant_efficiency.get_resource_efficiency_for_date(date=date(2020, 1, 1)) == 1
    assert constant_efficiency.get_resource_efficiency_for_date(date=date(2025, 1, 1)) == 1


def test_linear_growth_efficiency_returns_zero_before_start_date():
    linear_growth_efficiency = LinearGrowthEfficiency(start_date=date(2020, 1, 1),
                                                      full_efficiency_date=date(2020, 1, 10))

    assert linear_growth_efficiency.get_resource_efficiency_for_date(date=date(2019, 12, 31)) == 0.0


def test_linear_growth_efficiency_returns_one_after_end_date():
    linear_growth_efficiency = LinearGrowthEfficiency(start_date=date(2020, 1, 1),
                                                      full_efficiency_date=date(2020, 1, 10))

    assert linear_growth_efficiency.get_resource_efficiency_for_date(date=date(2020, 1, 11)) == 1.0


def test_linear_growth_efficiency_returns_interpolation_between_start_date_and_full_efficiency_date():
    linear_growth_efficiency = LinearGrowthEfficiency(start_date=date(2020, 1, 1),
                                                      full_efficiency_date=date(2020, 1, 10))

    assert linear_growth_efficiency.get_resource_efficiency_for_date(date=date(2020, 1, 5)) == 0.5


def test_linear_growth_efficiency_returns_one_if_start_date_greater_than_full_efficiency_date():
    linear_growth_efficiency = LinearGrowthEfficiency(start_date=date(2020, 1, 1),
                                                      full_efficiency_date=date(2019, 1, 1))
    assert linear_growth_efficiency.get_resource_efficiency_for_date(date=date(2019, 1, 1)) == 1.0

def test_time_bounded_constant_efficiency_returns_1_on_day_between_start_and_end():
    time_bounded_constant_efficiency = TimeBoundedConstantEfficiency(start_date=date(2021, 1, 1), end_date=date(2021, 12, 31))

    assert time_bounded_constant_efficiency.get_resource_efficiency_for_date(date=date(2021, 1, 1)) == 1
    assert time_bounded_constant_efficiency.get_resource_efficiency_for_date(date=date(2021, 12, 31)) == 1

def test_time_bounded_constant_efficiency_returns_0_on_day_outside_start_and_end():
    time_bounded_constant_efficiency = TimeBoundedConstantEfficiency(start_date=date(2021, 1, 1), end_date=date(2021, 12, 31))

    assert time_bounded_constant_efficiency.get_resource_efficiency_for_date(date=date(2020, 12, 31)) == 0
    assert time_bounded_constant_efficiency.get_resource_efficiency_for_date(date=date(2022, 1, 1)) == 0

def test_vacation_calendar_makes_working_day_a_holiday():
    vacation_calendar = VacationCalendar(holidays=[date(2020, 11, 5), date(2020, 11, 6)],
                                         working_days=[date(2020, 11, 7)], child_calendar=RussianCalendar())

    assert vacation_calendar.is_working_day(day=date(2020, 11, 3))
    assert not vacation_calendar.is_working_day(day=date(2020, 11, 4))
    assert not vacation_calendar.is_working_day(day=date(2020, 11, 5))
    assert vacation_calendar.is_working_day(day=date(2020, 11, 7))
    assert not vacation_calendar.is_working_day(day=date(2020, 11, 8))


def test_assignment_entry_holds_attributes():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 3 + 14)

    capacities = Capacities(
        work_hours_per_day=7.0,
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

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=team)

    assignment_entry = AssignmentEntry(
        task=task,
        resource=resource,
        date=date(2020, 10, 3),
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assert assignment_entry.task == task
    assert assignment_entry.resource == resource
    assert assignment_entry.date == date(2020, 10, 3)
    assert assignment_entry.skill == Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT)
    assert assignment_entry.task_effort_decrease_hours == 3.5
    assert assignment_entry.resource_spent_hours == 7


def test_assignment_entry_raises_value_error_if_resource_spent_hours_less_than_minimal_spendable_hours_or_not_divisible_by_minimal_spendable_hours_without_remainder():
    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 3 + 14)

    capacities = Capacities(
        work_hours_per_day=7.0,
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

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=team)

    less_than_minimal_spendable_hours = AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS * 0.99
    with pytest.raises(ValueError):
        _ = AssignmentEntry(
            task=task,
            resource=resource,
            date=date(2020, 10, 3),
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            task_effort_decrease_hours=0.2,
            resource_spent_hours=less_than_minimal_spendable_hours
        )

    not_divisible_by_minimal_spendable_hours = AssignmentEntry.MINIMAL_SPENDABLE_RESOURCE_HOURS * 5 * 0.99
    with pytest.raises(ValueError):
        _ = AssignmentEntry(
            task=task,
            resource=resource,
            date=date(2020, 10, 3),
            skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            task_effort_decrease_hours=0.2,
            resource_spent_hours=not_divisible_by_minimal_spendable_hours
        )

def test_quantize_resource_spent_hours_quantizes_time():
    assert quantize_resource_spent_hours(0.5) == 0.5
    assert quantize_resource_spent_hours(0.51) == 0.5
    assert quantize_resource_spent_hours(1.49) == 1.0

def test_assignments_holds_attributes():
    assignments = Assignments()
    assert len(assignments.assignment_list) == 0


def test_assignments_has_start_date_returns_false_if_no_assignments_in_list():
    assignments = Assignments()
    assert not assignments.has_start_date()


def test_assignments_get_start_date_raises_error_if_no_no_assignments_in_list():
    assignments = Assignments()
    with pytest.raises(ValueError):
        assignments.get_start_date()


def test_assignments_has_end_date_returns_false_if_no_assignments_in_list():
    assignments = Assignments()
    assert not assignments.has_end_date()


def test_assignments_get_end_date_raises_error_if_no_no_assignments_in_list():
    assignments = Assignments()
    with pytest.raises(ValueError):
        assignments.get_end_date()


def test_assignments_return_start_and_end_date():
    assignments = Assignments()

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

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=team)

    assignment_entry_1 = AssignmentEntry(
        task=task,
        resource=resource,
        date=date(2020, 10, 3),
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignment_entry_2 = AssignmentEntry(
        task=task,
        resource=resource,
        date=date(2020, 10, 8),
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignments.assignment_list = [assignment_entry_1, assignment_entry_2]

    assert assignments.has_start_date()
    assert assignments.has_end_date()
    assert assignments.get_start_date() == date(2020, 10, 3)
    assert assignments.get_end_date() == date(2020, 10, 8)


def test_assignments_get_resources_return_distinct_resources():
    assignments = Assignments()

    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 3 + 14)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource_1 = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    resource_2 = SimpleResource(id='buz@bar.com', name='Buz', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=team)

    assignment_entry_1 = AssignmentEntry(
        task=task,
        resource=resource_1,
        date=date(2020, 10, 3),
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignment_entry_2_1 = AssignmentEntry(
        task=task,
        resource=resource_2,
        date=date(2020, 10, 8),
        skill=Skill(system='Buz', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignment_entry_2_2 = AssignmentEntry(
        task=task,
        resource=resource_2,
        date=date(2020, 10, 8),
        skill=Skill(system='Buz', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignments.assignment_list = [assignment_entry_1, assignment_entry_2_1, assignment_entry_2_2]

    resources = assignments.get_resources()

    assert len(resources) == 2
    assert resource_1 in resources
    assert resource_2 in resources

def test_assignments_get_assignment_list_for_task_and_resource_returns_assignments():
    assignments = Assignments()

    work_date_start = date(2020, 10, 3)
    work_date_end = date(2020, 10, 3 + 14)

    capacities = Capacities(work_hours_per_day=7.0, calendar=RussianCalendar(),
                            efficiency_in_time=ConstantEfficiency())

    capacity_entry = CapacityEntry(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]

    resource_1 = SimpleResource(id='foo@bar.com', name='Foo', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    resource_2 = SimpleResource(id='buz@bar.com', name='Buz', work_date_start=work_date_start,
                            work_date_end=work_date_end,
                            business_line='BL-1',
                            capacities=capacities)

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=Efforts(effort_entries=[]), team=team)

    assignment_entry_1 = AssignmentEntry(
        task=task,
        resource=resource_1,
        date=date(2020, 10, 3),
        skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignment_entry_2_1 = AssignmentEntry(
        task=task,
        resource=resource_2,
        date=date(2020, 10, 8),
        skill=Skill(system='Buz', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignment_entry_2_2 = AssignmentEntry(
        task=task,
        resource=resource_2,
        date=date(2020, 10, 8),
        skill=Skill(system='Buz', ability=AbilityEnum.DEVELOPMENT),
        task_effort_decrease_hours=3.5,
        resource_spent_hours=7.0
    )

    assignments.assignment_list = [assignment_entry_1, assignment_entry_2_1, assignment_entry_2_2]

    assignment_entries = assignments.get_assignment_entries_for_task_and_resource(task=task, resource=resource_2)

    assert len(assignment_entries) == 2
    assert assignment_entry_2_1 in assignment_entries
    assert assignment_entry_2_2 in assignment_entries

def test_external_task_equals_by_attributes():
    external_task_1 = ExternalTask(
        id='CR-1',
        name='Change Request 1',
        system=''
    )

    external_task_1.efforts = [
        ExternalTaskEffort(
            ability=AbilityEnum.SYSTEM_ANALYSIS,
            hours=8
        ),
        ExternalTaskEffort(
            ability=AbilityEnum.DEVELOPMENT,
            hours=80
        )
    ]

    external_task_1_1 = ExternalTask(
        id='SYS-CR-1.1',
        name='System Change Request 1.1',
        system='SYS-1'
    )

    external_task_1_2 = ExternalTask(
        id='SYS-CR-1.2',
        name='System Change Request 1.2',
        system='SYS-2'
    )

    external_task_1.sub_tasks = [external_task_1_1, external_task_1_2]

    external_task_2 = ExternalTask(
        id='CR-1',
        name='Change Request 1',
        system=''
    )

    external_task_2.efforts = [
        ExternalTaskEffort(
            ability=AbilityEnum.DEVELOPMENT,
            hours=80
        ),
        ExternalTaskEffort(
            ability=AbilityEnum.SYSTEM_ANALYSIS,
            hours=8
        )
    ]

    external_task_2_1 = ExternalTask(
        id='SYS-CR-1.1',
        name='System Change Request 1.1',
        system='SYS-1'
    )

    external_task_2_2 = ExternalTask(
        id='SYS-CR-1.2',
        name='System Change Request 1.2',
        system='SYS-2'
    )

    external_task_2.sub_tasks = [external_task_2_2, external_task_2_1]

    assert external_task_1 == external_task_2
