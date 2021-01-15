from datetime import date

from Outputs.ResourceLackOutput import ResourceLackOutput
from Outputs.TaskOutput import TaskOutput
from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyOutput import TaskResourceSupplyOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanOutput import ResourceCalendarPlanOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationOutput import ResourceUtilizationOutput


class PlanOutput:

    def __init__(self, start_date: date, end_date: date):
        self.start_date: date = start_date
        self.end_date: date = end_date
        self.tasks: [TaskOutput] = []
        self.task_resource_supply: TaskResourceSupplyOutput = TaskResourceSupplyOutput()
        self.resource_calendar_plan: ResourceCalendarPlanOutput = ResourceCalendarPlanOutput()
        self.resource_utilization: ResourceUtilizationOutput = ResourceUtilizationOutput()
        self.resource_lacks: [ResourceLackOutput] = []

