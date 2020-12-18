from Entities.Plan.Plan import Plan
from Entities.RepositoryTask.ExternalTask import ExternalTask
from Entities.RepositoryTask.ExternalTaskEffort import ExternalTaskEffort
from Entities.Resource.Calendar.Calendar import generate_date_range
from Entities.Resource.Resource import Resource
from Entities.Task.Effort.Efforts import Efforts
from Entities.Task.FinishStartConstrainedTask import FinishStartConstrainedTask
from Entities.Task.Task import Task
from Entities.Team.Member import Member
from Inputs.EffortInput import EffortInput
from Inputs.TaskInput import TaskInput
from Inputs.TeamMemberInput import TeamMemberInput
from Interactors.ExternalTasksToExternalTaskOutputsConverter import ExternalTasksToExternalTaskOutputsConverter
from Outputs.EffortOutput import EffortOutput
from Outputs.ExternalTaskOutput import ExternalTaskOutput
from Outputs.HightlightOutput import HighlightOutput
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanBottleneckHintOutput import \
    ResourceCalendarPlanBottleneckHintOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanGroupOutput import ResourceCalendarPlanGroupOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanMemberOutput import ResourceCalendarPlanMemberOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanOutput import ResourceCalendarPlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanTaskOutput import ResourceCalendarPlanTaskOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationOutput import ResourceUtilizationOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationPercentOutput import ResourceUtilizationPercentOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationResourceOutput import ResourceUtilizationResourceOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationTaskOutput import ResourceUtilizationTaskOutput
from Outputs.TaskOutput import TaskOutput
from Outputs.TaskResourceSupplyOutputs.SkillResourceSupplyOutput import SkillResourceSupplyOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyOutput import TaskResourceSupplyOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyRowOutput import TaskResourceSupplyRowOutput
import datetime

from Outputs.TeamMemberOutput import TeamMemberOutput


class PlanOutputCreator:

    def __init__(self, plan: Plan, task_inputs: [TaskInput], external_tasks: [ExternalTask]):
        self.plan: Plan = plan
        self.task_inputs: [TaskInput] = task_inputs
        self.external_tasks: [ExternalTask] = external_tasks

    def calculate_task_completion(self, initial_effort: Efforts, remaining_effort: Efforts):
        result = []

        for initial in initial_effort.effort_entries:
            remaining_hours = remaining_effort.get_hours_for_skill(initial.skill)
            percentage = {
                'skill': initial.skill,
                'supply_percent': 1.0 - remaining_hours / initial.hours if initial.hours != 0 else 1.0
            }

            result.append(percentage)

        return result

    def convert_entities_to_task_supply(self, tasks: [Task]):
        result = TaskResourceSupplyOutput()

        for task in tasks:
            initial_effort_hours = task.get_initial_efforts_hours()
            remaining_effort_hours = task.get_remaining_efforts_hours()
            percent_complete =  remaining_effort_hours / initial_effort_hours if remaining_effort_hours > 0 else 1.0
            is_fully_supplied = percent_complete == 1.0
            highlight = HighlightOutput.REGULAR if is_fully_supplied else HighlightOutput.ERROR
            task_resource_supply_row = TaskResourceSupplyRowOutput(
                task_id=task.get_id(),
                task_name=task.get_name(),
                business_line=task.get_business_line(),
                is_fully_supplied=is_fully_supplied,
                is_fully_supplied_highlight=highlight
            )

            task_completion = self.calculate_task_completion(initial_effort=task.get_initial_efforts(), remaining_effort=task.get_remaining_efforts())

            for completion in task_completion:
                system = completion['skill'].system
                ability = completion['skill'].ability
                supply_percent = completion['supply_percent']
                highlight = HighlightOutput.REGULAR if supply_percent == 1.0 else HighlightOutput.ERROR
                skill_resource_supply = SkillResourceSupplyOutput(
                    system=system,
                    ability=ability,
                    supply_percent=supply_percent,
                    highlight=highlight
                )

                task_resource_supply_row.skill_resource_supply.append(skill_resource_supply)

            result.rows.append(task_resource_supply_row)

        return result

    def convert_task_members_to_member_outputs(self, members: [Member], task: Task):
        result = []

        for member in members:
            if member.has_picked_resource():
                resource = member.get_picked_resource()

                task_assignments = task.get_assignments()

                task_resource_assignment_entries = task_assignments.get_assignment_entries_for_task_and_resource(
                    task=task,
                    resource=resource
                )

                resource_dates = [assignment_entry.date for assignment_entry in task_resource_assignment_entries if assignment_entry.task_effort_decrease_hours > 0]

                start_date = min(resource_dates) if len(resource_dates) > 0 else ''
                start_date_highlight = HighlightOutput.REGULAR if len(resource_dates) > 0 else HighlightOutput.ERROR

                end_date = max(resource_dates) if len(resource_dates) > 0 else ''
                end_date_highlight = HighlightOutput.REGULAR if len(resource_dates) > 0 else HighlightOutput.ERROR
                effort_decrease_hours = sum([assignment_entry.task_effort_decrease_hours for assignment_entry in task_resource_assignment_entries])

                member_output = ResourceCalendarPlanMemberOutput(
                    resource_id=resource.id,
                    resource_name=resource.name,
                    highlight=HighlightOutput.REGULAR,
                    start_date_or_empty_string=start_date,
                    start_date_highlight=start_date_highlight,
                    end_date_or_empty_string=end_date,
                    end_date_highlight=end_date_highlight,
                    effort_decrease_hours=effort_decrease_hours
                )

                for assignment_entry in task_resource_assignment_entries:
                    member_output.effort_decreases_by_date[assignment_entry.date] = assignment_entry.task_effort_decrease_hours

                result.append(member_output)
            else:
                member_output = ResourceCalendarPlanMemberOutput(
                    resource_id='',
                    resource_name='',
                    highlight=HighlightOutput.ERROR,
                    start_date_or_empty_string='',
                    start_date_highlight=HighlightOutput.ERROR,
                    end_date_or_empty_string='',
                    end_date_highlight=HighlightOutput.ERROR,
                    effort_decrease_hours=0
                )

                result.append(member_output)

        return result

    def convert_task_groups_to_resource_outputs(self, task: Task):
        result = []
        team = task.get_team()
        groups = team.groups

        for group in groups:
            system = group.skill.system
            ability = group.skill.ability
            group_skill = group.skill
            initial_hours = task.get_initial_efforts_hours_for_skill_ignoring_sub_tasks(skill=group_skill)
            remaining_hours = task.get_remaining_efforts_hours_for_skill_ignoring_sub_tasks(skill=group_skill)
            planned_hours = initial_hours - remaining_hours
            planned_readiness = planned_hours / initial_hours if initial_hours > 0 else 1
            is_bottleneck = group.is_bottleneck

            if planned_readiness == 1.0:
                if is_bottleneck:
                    highlight = HighlightOutput.WARNING
                else:
                    highlight = HighlightOutput.REGULAR
            else:
                highlight = HighlightOutput.ERROR

            group_output = ResourceCalendarPlanGroupOutput(
                system=system,
                ability=ability,
                initial_hours=initial_hours,
                planned_hours=planned_hours,
                planned_readiness=planned_readiness,
                highlight=highlight,
                is_bottleneck=is_bottleneck
            )

            members = group.members

            group_output.members = self.convert_task_members_to_member_outputs(members=members, task=task)

            result.append(group_output)

        return result

    def convert_task_to_bottleneck_hints(self, task: Task) -> [ResourceCalendarPlanBottleneckHintOutput]:
        result = []

        team = task.get_team()
        groups = team.groups

        for group in groups:
            is_bottleneck = group.is_bottleneck

            if is_bottleneck:
                task_id = task.get_id()
                system = group.skill.system
                ability = group.skill.ability

                bottleneck_hint = ResourceCalendarPlanBottleneckHintOutput(
                    task_id=task_id,
                    system=system,
                    ability=ability
                )

                result.append(bottleneck_hint)

        sub_tasks = task.get_direct_sub_tasks()
        for sub_task in sub_tasks:
            result = result + self.convert_task_to_bottleneck_hints(task=sub_task)

        return result


    def convert_entities_to_tasks_output(self, tasks: [Task]):
        result: [ResourceCalendarPlanTaskOutput] = []

        for task in tasks:
            start_date = task.get_start_date() if task.has_start_date() else ''
            start_date_highlight = HighlightOutput.REGULAR if task.has_start_date() else HighlightOutput.ERROR
            end_date = task.get_end_date() if task.has_end_date() else ''
            end_date_highlight = HighlightOutput.REGULAR if task.has_end_date() else HighlightOutput.ERROR
            initial_effort_hours = task.get_initial_efforts().get_hours()
            remaining_effort_hours = task.get_remaining_efforts_hours()
            assigned_effort_hours = initial_effort_hours - remaining_effort_hours
            completion_percent = 1.0 - remaining_effort_hours / initial_effort_hours if initial_effort_hours > 0 else 1.0
            completion_percent_highlight = HighlightOutput.REGULAR if completion_percent == 1.0 else HighlightOutput.ERROR
            bottleneck_hints = self.convert_task_to_bottleneck_hints(task=task)

            task_output = ResourceCalendarPlanTaskOutput(
                id=task.get_id(),
                name=task.get_name(),
                business_line=task.get_business_line(),
                start_date_or_empty_string=start_date,
                start_date_highlight=start_date_highlight,
                end_date_or_empty_string=end_date,
                end_date_highlight=end_date_highlight,
                initial_effort_hours=initial_effort_hours,
                assigned_effort_hours=assigned_effort_hours,
                planned_readiness=completion_percent,
                planned_readiness_highlight=completion_percent_highlight,
            )
            task_output.bottleneck_hints = bottleneck_hints

            predecessors_ids: [] = [task.get_id() for task in task.predecessors] if isinstance(task, FinishStartConstrainedTask) else []
            task_output.predecessor_ids = predecessors_ids

            task_output.groups = self.convert_task_groups_to_resource_outputs(task=task)

            task_output.sub_tasks = self.convert_entities_to_tasks_output(tasks=task.get_direct_sub_tasks())

            result.append(task_output)


        return result

    def convert_entities_to_resource_calendar_plan(self, tasks: [Task]):
        result = ResourceCalendarPlanOutput()

        task_outputs = self.convert_entities_to_tasks_output(tasks)

        result.tasks = task_outputs

        return result

    def get_highlight_for_utilization_percent(self, utilization_percent: float):
        if utilization_percent > 0.95:
            return HighlightOutput.REGULAR
        elif utilization_percent > 0.0:
            return HighlightOutput.WARNING
        else:
            return HighlightOutput.ERROR

    def convert_entities_to_utilization_by_date(self, resource: Resource, start_date: datetime.date, end_date: datetime.date):
        result = {}

        for date in generate_date_range(start_date=start_date, end_date=end_date):
            initial_work_hours = resource.get_initial_work_hours_for_date(date=date)
            remaining_work_hours = resource.get_remaining_work_hours_for_date(date=date)
            utilization_percent = 1.0 - remaining_work_hours / initial_work_hours if initial_work_hours > 0 else 1.0
            highlight = self.get_highlight_for_utilization_percent(utilization_percent)
            utilization_percent_output = ResourceUtilizationPercentOutput(value=utilization_percent, highlight=highlight)
            result[date] = utilization_percent_output

        return result

    def convert_entities_to_resource_utilization_task_hours(self, resource: Resource, task: Task):
        result = {}

        assignment_entries = task.get_assignment_entries_for_resource(resource=resource)

        for assignment_entry in assignment_entries:
            date = assignment_entry.date
            resource_spent_hours = assignment_entry.resource_spent_hours
            result[date] = resource_spent_hours

        return result

    def convert_entities_to_resource_utilization_tasks(self, resource: Resource):
        result = []

        tasks = resource.get_tasks()

        for task in tasks:
            task_output = ResourceUtilizationTaskOutput(
                id=task.get_id(),
                name=task.get_name()
            )
            task_output.hours_spent_by_day = self.convert_entities_to_resource_utilization_task_hours(task=task, resource=resource)

            result.append(task_output)

        return result

    def convert_entities_to_resource_utilization(self, resources: [Resource], start_date: datetime.date, end_date: datetime.date):
        result = ResourceUtilizationOutput()

        for resource in resources:
            resource_output = ResourceUtilizationResourceOutput(
                id=resource.id,
                name=resource.name,
                business_line=resource.business_line
            )

            resource_output.utilization_by_date = self.convert_entities_to_utilization_by_date(resource=resource, start_date=start_date, end_date=end_date)

            resource_output.tasks = self.convert_entities_to_resource_utilization_tasks(resource=resource)

            result.resources.append(resource_output)

        return result

    def convert_effort_input_to_effort_output(self, effort_input: EffortInput) -> EffortOutput:
        return EffortOutput(
            ability=effort_input.ability,
            hours=effort_input.hours
        )

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def convert_team_member_input_to_team_member_output(self, team_member_input: TeamMemberInput) -> TeamMemberOutput:
        resource_ids_and_or_quantities_output = []

        for resource_id_and_or_quantity in team_member_input.resource_ids_and_or_quantities:
            if self.is_float(resource_id_and_or_quantity):
                resource_ids_and_or_quantities_output.append(float(resource_id_and_or_quantity))
            else:
                resource_ids_and_or_quantities_output.append(resource_id_and_or_quantity)

        return TeamMemberOutput(
            system=team_member_input.system,
            ability=team_member_input.ability,
            resource_ids_and_or_quantities=resource_ids_and_or_quantities_output
        )


    def convert_task_input_to_task_output_not_filling_predecessors(self, task_input: TaskInput) -> TaskOutput:
        result = TaskOutput(
            id=task_input.id,
            name=task_input.name,
            system=task_input.system,
            business_line=task_input.business_line
        )

        efforts = [self.convert_effort_input_to_effort_output(effort) for effort in task_input.efforts]
        result.efforts = efforts

        team_members = [self.convert_team_member_input_to_team_member_output(team_member) for team_member in task_input.team_members]
        result.team_members = team_members

        sub_tasks = [self.convert_task_input_to_task_output_not_filling_predecessors(sub_task) for sub_task in task_input.sub_tasks]
        result.sub_tasks = sub_tasks

        return result


    def convert_task_inputs_to_task_outputs_not_filling_predecessors(self, task_inputs: [TaskInput]) -> [TaskOutput]:
        return [self.convert_task_input_to_task_output_not_filling_predecessors(task_input) for task_input in task_inputs]

    def find_task_outputs_by_id_recursive(self, task_id: str, tasks: [TaskOutput]):
        result = []

        for task in tasks:
            if task.id == task_id:
                result.append(task)

            task_children_with_desired_task_id = self.find_task_outputs_by_id_recursive(task_id=task_id, tasks=task.sub_tasks)

            result = result + task_children_with_desired_task_id

        return result

    def find_task_output_by_id(self, task_id: str, tasks: [TaskOutput]) -> Task:
        found_tasks = self.find_task_outputs_by_id_recursive(task_id=task_id, tasks=tasks)

        if (len(found_tasks) == 1):
            return found_tasks[0]
        else:
            raise ValueError('Must be exactly one task with id "{}", but {} found'.format(task_id, len(found_tasks)))

    def fill_predecessors_in_task_outputs_recursive(self, task_inputs_containing_predecessor_data: [TaskInput], tasks_that_will_receive_predecessors: [TaskOutput]):
        for task_input in task_inputs_containing_predecessor_data:
            has_predecessors = len(task_input.predecessors) > 0
            if has_predecessors:
                task_id = task_input.id
                predecessor_input_ids = [predecessor.id for predecessor in task_input.predecessors]

                task = self.find_task_output_by_id(task_id=task_id, tasks=tasks_that_will_receive_predecessors)
                for predecessor_input_ids in predecessor_input_ids:
                    predecessor = self.find_task_output_by_id(task_id=predecessor_input_ids, tasks=tasks_that_will_receive_predecessors)
                    task.predecessors.append(predecessor)

            self.fill_predecessors_in_task_outputs_recursive(task_inputs_containing_predecessor_data=task_input.sub_tasks, tasks_that_will_receive_predecessors=tasks_that_will_receive_predecessors)


    def convert_task_inputs_to_task_outputs(self, task_inputs: [TaskInput]) -> [TaskOutput]:
        result = self.convert_task_inputs_to_task_outputs_not_filling_predecessors(task_inputs=task_inputs)
        self.fill_predecessors_in_task_outputs_recursive(task_inputs_containing_predecessor_data=task_inputs, tasks_that_will_receive_predecessors=result)
        return result

    def create_output(self):
        result = PlanOutput(start_date=self.plan.start_date, end_date=self.plan.end_date)
        result.task_resource_supply = self.convert_entities_to_task_supply(tasks=self.plan.tasks)
        result.resource_calendar_plan = self.convert_entities_to_resource_calendar_plan(tasks=self.plan.tasks)
        result.resource_utilization = self.convert_entities_to_resource_utilization(
            resources=self.plan.resources,
            start_date=self.plan.start_date,
            end_date=self.plan.end_date
        )
        task_inputs = self.task_inputs
        result.tasks = self.convert_task_inputs_to_task_outputs(task_inputs=task_inputs)

        external_tasks = self.external_tasks
        convert_external_tasks_to_external_task_outputs = ExternalTasksToExternalTaskOutputsConverter(external_tasks=external_tasks)
        result.external_tasks = convert_external_tasks_to_external_task_outputs.convert()
        return result