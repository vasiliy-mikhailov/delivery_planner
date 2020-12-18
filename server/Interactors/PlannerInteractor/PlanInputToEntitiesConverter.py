from collections import Counter

from Entities.Resource.Calendar.BelarusCalendar import BelarusCalendar
from Entities.Resource.Calendar.Calendar import generate_date_range, Calendar
from Entities.Resource.Calendar.RussianCalendar import RussianCalendar
from Entities.Resource.Calendar.VacationCalendar import VacationCalendar
from Entities.Resource.Capacity.Capacities import Capacities
from Entities.Resource.Capacity.CapacityEntry import CapacityEntry
from Entities.Resource.EfficiencyInTime.ConstantEfficiency import ConstantEfficiency
from Entities.Resource.EfficiencyInTime.LinearGrowthEfficiency import LinearGrowthEfficiency
from Entities.Resource.Resource import Resource
from Entities.Resource.SimpleResource import SimpleResource
from Entities.Skill.Skill import Skill
from Entities.Task.Effort.Effort import Effort
from Entities.Task.Effort.Efforts import Efforts
from Entities.Task.FinishStartConstrainedTask import FinishStartConstrainedTask
from Entities.Task.SimpleTask import SimpleTask
from Entities.Task.Task import Task
from Entities.Team.ConcreteResourceMember import ConcreteResourceMember
from Entities.Team.InconcreteResourceMember import InconcreteResourceMember
from Entities.Team.Team import Team
from Inputs.CapacityInput import CapacityInput
from Inputs.EffortInput import EffortInput
from Inputs.PlanInput import PlanInput
from Inputs.TaskInput import TaskInput
import datetime

class PlanInputToEntitiesConverter:

    def __init__(self,  plan_input: PlanInput):
        self.plan_input = plan_input

    def convert_effort_inputs_to_entity(self, system: str, effort_inputs: [EffortInput]):
        return Efforts(
            effort_entries=[Effort(skill=Skill(system=system, ability=effort_input.ability), hours=effort_input.hours) for effort_input in
                            effort_inputs])

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def make_team_from_task_input_only(self, task_input: TaskInput, resources: [Resource]) -> Team:
        business_line = task_input.business_line
        result = Team(business_line=business_line)
        result.resource_pool = resources
        team_members = task_input.team_members

        for team_member_input in team_members:
            for resource_id_and_or_quantity in team_member_input.resource_ids_and_or_quantities:
                system = team_member_input.system
                ability = team_member_input.ability
                if self.is_float(resource_id_and_or_quantity):
                    quantity = int(float(resource_id_and_or_quantity))
                    for _ in range(quantity):
                        member = InconcreteResourceMember(
                            business_line=business_line,
                            skill=Skill(system=system, ability=ability)
                        )
                        result.add_member(member=member)
                else:
                    resource_id = resource_id_and_or_quantity
                    resource = self.find_resource_by_id(resource_id=resource_id, resources=resources)
                    member = ConcreteResourceMember(
                        skill=Skill(system=system, ability=ability),
                        concrete_resource=resource
                    )
                    result.add_member(member=member)

        return result

    def convert_task_inputs_to_tasks_not_filling_predecessors(self, task_inputs: [TaskInput], resources: [Resource]):
        result = []
        for task_input in task_inputs:
            efforts = self.convert_effort_inputs_to_entity(system=task_input.system, effort_inputs=task_input.efforts)

            team = self.make_team_from_task_input_only(task_input=task_input, resources=resources)

            task = SimpleTask(
                id=task_input.id,
                name=task_input.name,
                business_line=task_input.business_line,
                efforts=efforts,
                team=team
            )

            for skill in task.get_initial_efforts_ignoring_sub_tasks().get_skills():
                if not team.has_group_for_skill(skill=skill):
                    one_member_for_skilled_effort = InconcreteResourceMember(
                        business_line=task.get_business_line(),
                        skill=skill
                    )
                    team.add_member(member=one_member_for_skilled_effort)

            task_has_predecessors = len(task_input.predecessors) > 0

            if task_has_predecessors:
                task = FinishStartConstrainedTask(
                    task=task
                )

            task.set_direct_sub_tasks(sub_tasks=self.convert_task_inputs_to_tasks_not_filling_predecessors(
                task_inputs=task_input.sub_tasks,
                resources=resources)
            )
            result.append(task)
        return result

    def fill_predecessors_in_tasks_recursive(self, task_inputs_containing_predecessor_data: [TaskInput], tasks_that_will_receive_predecessors: [Task]):
        for task_input in task_inputs_containing_predecessor_data:
            has_predecessors = len(task_input.predecessors) > 0
            if has_predecessors:
                task_id = task_input.id
                predecessor_input_ids = [predecessor.id for predecessor in task_input.predecessors]

                task = self.find_task_by_id(task_id=task_id, tasks=tasks_that_will_receive_predecessors)
                for predecessor_input_ids in predecessor_input_ids:
                    predecessor = self.find_task_by_id(task_id=predecessor_input_ids, tasks=tasks_that_will_receive_predecessors)
                    task.predecessors.append(predecessor)

            self.fill_predecessors_in_tasks_recursive(task_input.sub_tasks, tasks_that_will_receive_predecessors=tasks_that_will_receive_predecessors)

    def convert_task_inputs_to_tasks(self, task_inputs: [TaskInput], resources: [Resource]):
        result = self.convert_task_inputs_to_tasks_not_filling_predecessors(task_inputs=task_inputs, resources=resources)
        self.fill_predecessors_in_tasks_recursive(tasks_that_will_receive_predecessors=result, task_inputs_containing_predecessor_data=task_inputs)
        return result

    def create_calendar_for_code(self, calendar_code: str) -> Calendar:
        if calendar_code == 'RU':
            return RussianCalendar()
        elif calendar_code == 'BY':
            return BelarusCalendar()
        else:
            raise ValueError('Invalid calendar code {}'.format(calendar_code))

    def convert_vacations_to_date_array(self, resource_id: str) -> [datetime.date]:
        result = []
        for vacation in self.plan_input.vacations:
            if vacation.resource_id == resource_id:
                for date in generate_date_range(start_date=vacation.start_date, end_date=vacation.end_date):
                    result.append(date)

        return result

    def convert_capacities_to_entities(self, capacities_input: [CapacityInput]):
        result = []

        for capacity_per_day in capacities_input:
            capacity_entry = CapacityEntry(
                skill=Skill(system=capacity_per_day.system, ability=capacity_per_day.ability),
                efficiency=capacity_per_day.efficiency
            )
            result.append(capacity_entry)

        return result

    def get_duplicates_in_existing_resource_ids(self) -> bool:
        resource_ids = [existing_resource.id for existing_resource in self.plan_input.existing_resources]
        result = [id for id, count in Counter(resource_ids).items() if count > 1]

        return result


    def convert_existing_resources_to_entities(self) -> [SimpleResource]:
        result = []

        duplicated_resource_ids = self.get_duplicates_in_existing_resource_ids()
        if duplicated_resource_ids:
            raise ValueError("PlannerInteractor convert_existing_resources_to_entities duplicate resource ids found {}".format(duplicated_resource_ids))

        for existing_resource_input in self.plan_input.existing_resources:
            calendar_code = existing_resource_input.calendar
            national_calendar = self.create_calendar_for_code(calendar_code=calendar_code)
            holidays = self.convert_vacations_to_date_array(resource_id=existing_resource_input.id)
            vacation_calendar = VacationCalendar(holidays=holidays, working_days=[],
                                                 child_calendar=national_calendar)

            capacities = Capacities(work_hours_per_day=existing_resource_input.hours_per_day, calendar=vacation_calendar,
                                    efficiency_in_time=ConstantEfficiency())

            capacities.capacity_list = self.convert_capacities_to_entities(existing_resource_input.capacity_per_day)


            person_resource = SimpleResource(
                id=existing_resource_input.id,
                name=existing_resource_input.name,
                work_date_start=self.plan_input.start_date,
                work_date_end=self.plan_input.end_date,
                business_line=existing_resource_input.business_line,
                capacities=capacities
            )

            result.append(person_resource)

        return result

    def convert_planned_resources_to_entities(self) -> [SimpleResource]:
        result = []

        for planned_resource_input in self.plan_input.planned_resources:
            calendar_code = planned_resource_input.calendar
            calendar = self.create_calendar_for_code(calendar_code=calendar_code)
            linear_growth_efficiency = LinearGrowthEfficiency(
                start_date=planned_resource_input.start_date,
                full_efficiency_date=planned_resource_input.start_date + datetime.timedelta(
                    days=int(30.0 * planned_resource_input.full_power_in_month))
            )

            capacities = Capacities(work_hours_per_day=planned_resource_input.hours_per_day, calendar=calendar,
                                    efficiency_in_time=linear_growth_efficiency)

            capacities.capacity_list = self.convert_capacities_to_entities(planned_resource_input.capacity_per_day)

            person_resource = SimpleResource(
                id=planned_resource_input.id,
                name=planned_resource_input.name,
                work_date_start=max(self.plan_input.start_date, planned_resource_input.start_date),
                work_date_end=self.plan_input.end_date,
                business_line=planned_resource_input.business_line,
                capacities=capacities
            )

            result.append(person_resource)

        return result

    def convert_input_resources_to_entities(self) -> [SimpleResource]:
        existing_resources = self.convert_existing_resources_to_entities()
        planned_resources = self.convert_planned_resources_to_entities()

        return existing_resources + planned_resources

    def find_tasks_by_id_recursive(self, task_id: str, tasks: [Task]):
        result = []

        for task in tasks:
            if task.get_id() == task_id:
                result.append(task)

            task_children_with_desired_task_id = self.find_tasks_by_id_recursive(task_id=task_id, tasks=task.get_direct_sub_tasks())

            result = result + task_children_with_desired_task_id

        return result

    def find_task_by_id(self, task_id: str, tasks: [Task]) -> Task:
        found_tasks = self.find_tasks_by_id_recursive(task_id=task_id, tasks=tasks)

        if (len(found_tasks) == 1):
            return found_tasks[0]
        else:
            raise ValueError('Must be exactly one task with id "{}", but {} found'.format(task_id, len(found_tasks)))

    def find_resource_by_id(self, resource_id: str, resources: [Resource]):
        found_resources = [resource for resource in resources if resource.id == resource_id]

        if (len(found_resources) == 1):
            return found_resources[0]
        else:
            raise ValueError()
