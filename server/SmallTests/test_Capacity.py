from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Resource.Capacity.Capacities import Capacities
from Entities.Resource.Capacity.CapacityEntry import CapacityEntry
from Entities.Resource.EfficiencyInTime.ConstantEfficiency import ConstantEfficiency
from Entities.Skill.AbilityEnum import AbilityEnum
from Entities.Skill.Skill import Skill
from Entities.Task.Effort.Effort import Effort
from Entities.Task.Effort.Efforts import Efforts
from Entities.Task.SimpleTask import SimpleTask
from Entities.Team.Team import Team
import datetime


def test_capacity_entry_holds_attributes():
    capacity_entry = CapacityEntry(Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE), efficiency=1.0)
    assert capacity_entry.skill == Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE)
    assert capacity_entry.efficiency == 1.0

def test_capacity_entry_is_helpful_for_task_returns_true_if_same_system():
    capacity_entry = CapacityEntry(Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=1.0)

    efforts = Efforts(
        effort_entries=[Effort(
            Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT),
            hours=100.0)]
    )

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    assert capacity_entry.is_helpful_in_performing_task(task=task)


def test_capacity_entry_is_helpful_for_task_returns_false_if_different_system():
    capacity_entry = CapacityEntry(Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT), efficiency=7.0)
    efforts = Efforts(
        effort_entries=[Effort(Skill(system='Different System', ability=AbilityEnum.DEVELOPMENT), hours=7.0)])

    team = Team(business_line='BL-1')

    task = SimpleTask(id='T-1', name='Task-1', business_line='BL-1', efforts=efforts, team=team)

    assert not capacity_entry.is_helpful_in_performing_task(task=task)

def test_capacities_holds_attributes():
    calendar = RussianCalendar()
    efficiency_in_time = ConstantEfficiency()
    capacities = Capacities(work_hours_per_day=7.0, calendar=calendar, efficiency_in_time=efficiency_in_time)
    assert capacities.work_hours_per_day == 7
    assert capacities.efficiency_in_time == efficiency_in_time
    assert len(capacities.capacity_list) == 0


def test_capacities_calculates_work_hours_for_date():
    calendar = RussianCalendar()
    efficiency_in_time = ConstantEfficiency()
    capacities = Capacities(work_hours_per_day=7.0, calendar=calendar, efficiency_in_time=efficiency_in_time)

    assert capacities.get_work_hours_for_date(date=datetime.date(2020, 10, 1)) == 7
    assert capacities.get_work_hours_for_date(date=datetime.date(2020, 11, 4)) == 0


def test_capacities_has_skill_returns_true_if_has_skill_and_false_otherwise():
    calendar = RussianCalendar()
    efficiency_in_time = ConstantEfficiency()
    capacities = Capacities(work_hours_per_day=7.0, calendar=calendar, efficiency_in_time=efficiency_in_time)
    capacity_entry = CapacityEntry(Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE), efficiency=1.0)
    capacities.capacity_list = [capacity_entry]
    assert capacities.has_skill(skill=Skill(system='Foo', ability=AbilityEnum.SOLUTION_ARCHITECTURE))
    assert not capacities.has_skill(skill=Skill(system='Bar', ability=AbilityEnum.SOLUTION_ARCHITECTURE))
    assert not capacities.has_skill(skill=Skill(system='Foo', ability=AbilityEnum.DEVELOPMENT))