from Outputs.HightlightOutput import HighlightOutput


class ResourceUtilizationPercentOutput:

    def __init__(self, value: float, highlight: HighlightOutput):
        self.value: float = value
        self.highlight: HighlightOutput = highlight
