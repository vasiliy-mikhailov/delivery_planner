from Outputs.HightlightOutput import HighlightOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanBottleneckHintOutput import \
    ResourceCalendarPlanBottleneckHintOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanGroupOutput import ResourceCalendarPlanGroupOutput


class ResourceCalendarPlanTaskOutput:

    def __init__(
            self,
            id: str,
            name: str,
            business_line: str,
            start_date_or_empty_string,
            start_date_highlight: HighlightOutput,
            end_date_or_empty_string,
            end_date_highlight: HighlightOutput,
            initial_effort_hours: float,
            assigned_effort_hours: float,
            planned_readiness: float,
            planned_readiness_highlight: HighlightOutput,
    ):
        self.id: str = id
        self.name: str = name
        self.business_line: str = business_line
        self.start_date_or_empty_string = start_date_or_empty_string
        self.start_date_highlight: HighlightOutput = start_date_highlight
        self.end_date_or_empty_string = end_date_or_empty_string
        self.end_date_highlight: HighlightOutput = end_date_highlight
        self.initial_effort_hours: float = initial_effort_hours
        self.assigned_effort_hours: float = assigned_effort_hours
        self.planned_readiness: float = planned_readiness
        self.planned_readiness_highlight: HighlightOutput = planned_readiness_highlight
        self.sub_tasks: [] = []
        self.groups: [ResourceCalendarPlanGroupOutput] = []
        self.predecessor_ids: [str] = []
        self.bottleneck_hints: [ResourceCalendarPlanBottleneckHintOutput] = []
