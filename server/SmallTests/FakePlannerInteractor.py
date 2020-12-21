from datetime import date
from Entities.Resource.Calendar.Calendar import generate_date_range
from Inputs.PlanInput import PlanInput
from Outputs.EffortOutput import EffortOutput
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanBottleneckHintOutput import \
    ResourceCalendarPlanBottleneckHintOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanGroupOutput import ResourceCalendarPlanGroupOutput
from Outputs.TaskOutput import TaskOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyOutput import TaskResourceSupplyOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanOutput import ResourceCalendarPlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanMemberOutput import ResourceCalendarPlanMemberOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationOutput import ResourceUtilizationOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyRowOutput import TaskResourceSupplyRowOutput
from Outputs.TaskResourceSupplyOutputs.SkillResourceSupplyOutput import SkillResourceSupplyOutput
from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.HightlightOutput import HighlightOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanTaskOutput import ResourceCalendarPlanTaskOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationPercentOutput import ResourceUtilizationPercentOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationResourceOutput import ResourceUtilizationResourceOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationTaskOutput import ResourceUtilizationTaskOutput
from Outputs.TeamMemberOutput import TeamMemberOutput


class FakePlanner:

    def generate_task_resource_supply_row(self, task_id: str, task_name: str, business_line: str, is_fully_supplied: bool, skill_supply_percent_list: []):
        task_resource_supply_row = TaskResourceSupplyRowOutput(
            task_id=task_id,
            task_name=task_name,
            business_line=business_line,
            is_fully_supplied=is_fully_supplied,
            is_fully_supplied_highlight=(HighlightOutput.REGULAR if is_fully_supplied else HighlightOutput.ERROR)
        )

        task_resource_supply_row.skill_resource_supply = [
            SkillResourceSupplyOutput(
                system=skill_supply_element['system'],
                ability=skill_supply_element['ability'],
                supply_percent=skill_supply_element['supply_percent'],
                highlight=skill_supply_element['highlight']
            ) for skill_supply_element in skill_supply_percent_list
        ]


        return task_resource_supply_row

    def generate_task_resource_supply(self):
        result = TaskResourceSupplyOutput()
        result.rows.append(self.generate_task_resource_supply_row(task_id='CR-1', task_name='Change Request 1', business_line='BL-1', is_fully_supplied=True, skill_supply_percent_list=[
            {'ability': AbilityEnum.SOLUTION_ARCHITECTURE, 'system': '', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.SYSTEM_ANALYSIS, 'system': 'SYS-1', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.SYSTEM_ANALYSIS, 'system': 'SYS-2', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.DEVELOPMENT, 'system': 'SYS-1', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.DEVELOPMENT, 'system': 'SYS-2', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.SYSTEM_TESTING, 'system': 'SYS-1', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.SYSTEM_TESTING, 'system': 'SYS-2', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.INTEGRATION_TESTING, 'system': '', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.PRODUCT_OWNERSHIP, 'system': '', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.PROJECT_MANAGEMENT, 'system': '', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR}
        ]))
        result.rows.append(self.generate_task_resource_supply_row(task_id='CR-2', task_name='Change Request 2', business_line='BL-2', is_fully_supplied=False, skill_supply_percent_list=[
            {'ability': AbilityEnum.SOLUTION_ARCHITECTURE, 'system': '', 'supply_percent': 0.0, 'highlight': HighlightOutput.ERROR},
            {'ability': AbilityEnum.SYSTEM_ANALYSIS, 'system': 'SYS-1', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.DEVELOPMENT, 'system': 'SYS-1', 'supply_percent': 0.1, 'highlight': HighlightOutput.ERROR},
            {'ability': AbilityEnum.SYSTEM_TESTING, 'system': 'SYS-2', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.INTEGRATION_TESTING, 'system': '', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR},
            {'ability': AbilityEnum.PROJECT_MANAGEMENT, 'system': '', 'supply_percent': 1.0, 'highlight': HighlightOutput.REGULAR}
        ]))

        return result

    def generate_resource_calendar_plan(self):
        result = ResourceCalendarPlanOutput()

        task_1 = ResourceCalendarPlanTaskOutput(
            id='CR-1',
            name='Заявка на доработку ПО',
            business_line='BL-1',
            start_date_or_empty_string=date(2020, 10, 5),
            start_date_highlight=HighlightOutput.REGULAR,
            end_date_or_empty_string=date(2021, 4, 16),
            end_date_highlight=HighlightOutput.REGULAR,
            initial_effort_hours=2520.0,
            assigned_effort_hours=2520.0,
            planned_readiness=1.0,
            planned_readiness_highlight=HighlightOutput.REGULAR,
        )
        task_1.bottleneck_hints = [ResourceCalendarPlanBottleneckHintOutput(
            task_id='CR-1',
            system='SYS-1',
            ability=AbilityEnum.DEVELOPMENT
        )]

        task_1_1 = ResourceCalendarPlanTaskOutput(
            id='SOLAR-1.1',
            name='Архитектура решения',
            business_line='',
            start_date_or_empty_string=date(2020, 11, 5),
            start_date_highlight=HighlightOutput.REGULAR,
            end_date_or_empty_string='',
            end_date_highlight=HighlightOutput.ERROR,
            initial_effort_hours=81.9,
            assigned_effort_hours=84.645,
            planned_readiness=0.95,
            planned_readiness_highlight=HighlightOutput.ERROR
        )

        group_1_1_1 = ResourceCalendarPlanGroupOutput(
            system='SYS-1',
            ability=AbilityEnum.SOLUTION_ARCHITECTURE,
            initial_hours=100,
            planned_hours=80,
            planned_readiness=0.8,
            highlight=HighlightOutput.ERROR,
            is_bottleneck=True
        )

        task_1_1.groups = [group_1_1_1]

        member_1_1_1 = ResourceCalendarPlanMemberOutput(
            resource_id='SOLAR-1',
            resource_name='Архитектор Р.А.',
            highlight=HighlightOutput.REGULAR,
            start_date_or_empty_string=date(2020, 11, 5),
            start_date_highlight=HighlightOutput.REGULAR,
            end_date_or_empty_string='',
            end_date_highlight=HighlightOutput.ERROR,
            effort_decrease_hours=12.0
        )

        member_1_1_1.effort_decreases_by_date[date(2020, 10, 5)] = 7.0
        member_1_1_1.effort_decreases_by_date[date(2020, 10, 7)] = 5.0

        group_1_1_1.members = [member_1_1_1]

        task_1_2 = ResourceCalendarPlanTaskOutput(
            id='SYSCR-1.1',
            name='Доработка системы',
            business_line='',
            start_date_or_empty_string=date(2020, 11, 5),
            start_date_highlight=HighlightOutput.REGULAR,
            end_date_or_empty_string='',
            end_date_highlight=HighlightOutput.ERROR,
            initial_effort_hours=220.69,
            assigned_effort_hours=209.6555,
            planned_readiness=0.95,
            planned_readiness_highlight=HighlightOutput.ERROR
        )

        task_1_2.predecessor_ids=['SOLAR-1.1']

        task_1_2_1 = ResourceCalendarPlanTaskOutput(
            id='SYSAN-1.1.1',
            name='Системная аналитика',
            business_line='',
            start_date_or_empty_string=date(2020, 11, 5),
            start_date_highlight=HighlightOutput.REGULAR,
            end_date_or_empty_string='',
            end_date_highlight=HighlightOutput.ERROR,
            initial_effort_hours=36.16,
            assigned_effort_hours=13.7408,
            planned_readiness=0.38,
            planned_readiness_highlight=HighlightOutput.ERROR,
        )

        task_1_2.sub_tasks = [task_1_2_1]

        task_1.sub_tasks = [task_1_1, task_1_2]

        task_2 = ResourceCalendarPlanTaskOutput(
            id='CR-2',
            name='Заявка на доработку ПО',
            business_line='BL-2',
            start_date_or_empty_string='',
            start_date_highlight=HighlightOutput.ERROR,
            end_date_or_empty_string='',
            end_date_highlight=HighlightOutput.ERROR,
            initial_effort_hours=230.0,
            assigned_effort_hours=115,
            planned_readiness=0.5,
            planned_readiness_highlight=HighlightOutput.ERROR
        )

        result.tasks = [task_1, task_2]

        return result

    def generate_resource_utilization(self, start_date: date, end_date: date):
        result = ResourceUtilizationOutput()

        resource = ResourceUtilizationResourceOutput(
            id='DEV-1',
            name='Developer',
            business_line='BL-1'
        )

        for date in generate_date_range(start_date, end_date):
            utilization_percent_output = ResourceUtilizationPercentOutput(value=1.0, highlight=HighlightOutput.REGULAR)
            resource.utilization_by_date[date] = utilization_percent_output

        task = ResourceUtilizationTaskOutput(
            id='CR-1',
            name='Change Request 1'
        )

        for date in generate_date_range(start_date, end_date):
            hours_spent = 7
            task.hours_spent_by_day[date] = hours_spent

        resource.tasks = [task]

        result.resources = [resource]

        return result

    def generate_first_task_output(self) -> TaskOutput:
        task_1 = TaskOutput(id='CR-1', name='Change Request 1', system='', business_line='BL-1')
        task_1.efforts = [
            EffortOutput(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=80.0),
            EffortOutput(ability=AbilityEnum.INTEGRATION_TESTING, hours=40.0),
            EffortOutput(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=80.0)
        ]

        task_1_1 = TaskOutput(id='SYSCR-1.1', name='System Change Request 1.1', system='SYS-1', business_line='BL-1')
        task_1_1.efforts = [
        ]

        task_1_1_1 = TaskOutput(id='SYSAN-1.1.1', name='System Analysis 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_1.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0)
        ]
        task_1_1_2 = TaskOutput(id='DEV-1.1.1', name='Development 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_2.efforts = [
            EffortOutput(ability=AbilityEnum.DEVELOPMENT, hours=120.0)
        ]
        task_1_1_2.predecessors = [task_1_1_1]

        task_1_1_3 = TaskOutput(id='SYSTEST-1.1.1', name='System Testing 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_3.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]
        task_1_1_3.predecessors = [task_1_1_2]

        task_1_1.sub_tasks = [task_1_1_1, task_1_1_2, task_1_1_3]

        task_1_2 = TaskOutput(id='SYSCR-1.2', name='System Change Request 1.2', system='SYS-2', business_line='BL-1')
        task_1_2.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=400.0),
            EffortOutput(ability=AbilityEnum.DEVELOPMENT, hours=1200),
            EffortOutput(ability=AbilityEnum.SYSTEM_TESTING, hours=400.0)
        ]

        task_1_2.team_members = [
            TeamMemberOutput(
                system='SYS-2',
                ability=AbilityEnum.SYSTEM_ANALYSIS,
                resource_ids_and_or_quantities=['solar@my.com']
            ),
            TeamMemberOutput(
                system='SYS-2',
                ability=AbilityEnum.DEVELOPMENT,
                resource_ids_and_or_quantities=[1]
            ),
        ]

        task_1.sub_tasks = [
            task_1_1,
            task_1_2
        ]

        return task_1

    def generate_second_task_Output(self) -> TaskOutput:
        task_2 = TaskOutput(id='CR-2', name='Change Request 2', system='', business_line='BL-2')
        task_2.efforts = [
            EffortOutput(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=8.0),
            EffortOutput(ability=AbilityEnum.INTEGRATION_TESTING, hours=2.0),
            EffortOutput(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=10.0)
        ]
        task_2_1 = TaskOutput(id='SYSCR-2.1', name='System Change Request 2.1', system='SYS-1', business_line='BL-2')
        task_2_1.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0),
            EffortOutput(ability=AbilityEnum.DEVELOPMENT, hours=120.0),
            EffortOutput(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]
        task_2.sub_tasks = [
            task_2_1
        ]

        return task_2

    def generate_task_outputs(self) -> [TaskOutput]:
        task_1 = self.generate_first_task_output()
        task_2 = self.generate_second_task_Output()
        return [task_1, task_2]

    def generate_first_external_task_output(self) -> TaskOutput:
        task_1 = TaskOutput(id='CR-1', name='Change Request 1', system='', business_line='BL-1')
        task_1.efforts = [
            EffortOutput(ability=AbilityEnum.SOLUTION_ARCHITECTURE, hours=80.0),
            EffortOutput(ability=AbilityEnum.INTEGRATION_TESTING, hours=40.0),
            EffortOutput(ability=AbilityEnum.PRODUCT_OWNERSHIP, hours=80.0)
        ]

        task_1_1 = TaskOutput(id='SYSCR-1.1', name='System Change Request 1.1', system='SYS-1', business_line='BL-1')
        task_1_1.efforts = [
        ]

        task_1_1_1 = TaskOutput(id='SYSAN-1.1.1', name='System Analysis 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_1.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=40.0)
        ]
        task_1_1_2 = TaskOutput(id='DEV-1.1.1', name='Development 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_2.efforts = [
            EffortOutput(ability=AbilityEnum.DEVELOPMENT, hours=120.0)
        ]

        task_1_1_3 = TaskOutput(id='SYSTEST-1.1.1', name='System Testing 1.1', system='SYS-1', business_line='BL-1')
        task_1_1_3.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_TESTING, hours=40.0)
        ]

        task_1_1.sub_tasks = [task_1_1_1, task_1_1_2, task_1_1_3]

        task_1_2 = TaskOutput(id='SYSCR-1.2', name='System Change Request 1.2', system='SYS-2', business_line='BL-1')
        task_1_2.efforts = [
            EffortOutput(ability=AbilityEnum.SYSTEM_ANALYSIS, hours=400.0),
            EffortOutput(ability=AbilityEnum.DEVELOPMENT, hours=1200),
            EffortOutput(ability=AbilityEnum.SYSTEM_TESTING, hours=400.0)
        ]

        task_1.sub_tasks = [
            task_1_1,
            task_1_2
        ]

        return task_1


    def plan(self, plan_input: PlanInput):
        start_date = plan_input.start_date
        end_date = plan_input.end_date
        plan_output = PlanOutput(start_date=start_date, end_date=end_date)
        plan_output.tasks = self.generate_task_outputs()
        plan_output.task_resource_supply = self.generate_task_resource_supply()
        plan_output.resource_calendar_plan = self.generate_resource_calendar_plan()
        plan_output.resource_utilization = self.generate_resource_utilization(start_date=start_date, end_date=end_date)
        plan_output.external_tasks = [
            self.generate_first_external_task_output()
        ]

        return plan_output