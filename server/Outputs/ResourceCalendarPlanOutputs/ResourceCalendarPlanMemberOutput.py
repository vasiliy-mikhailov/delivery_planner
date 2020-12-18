from Outputs.HightlightOutput import HighlightOutput


class ResourceCalendarPlanMemberOutput:

    def __init__(
            self,
            resource_id: str,
            resource_name: str,
            highlight: HighlightOutput,
            start_date_or_empty_string,
            start_date_highlight: HighlightOutput,
            end_date_or_empty_string,
            end_date_highlight: HighlightOutput,
            effort_decrease_hours: float
        ):
        self.resource_id: str = resource_id
        self.resource_name: str = resource_name
        self.highlight = highlight
        self.start_date_or_empty_string = start_date_or_empty_string
        self.start_date_highlight = start_date_highlight
        self.end_date_or_empty_string = end_date_or_empty_string
        self.end_date_highlight = end_date_highlight
        self.effort_decrease_hours: float = effort_decrease_hours
        self.effort_decreases_by_date: {} = {}

