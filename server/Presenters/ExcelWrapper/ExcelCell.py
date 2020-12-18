import math
from datetime import date
from Outputs.HightlightOutput import HighlightOutput


class ExcelCell:

    def __init__(self, value: object, format: dict = {}):
        if isinstance(value, float) and math.isnan(value):
            raise ValueError('ExcelCell __init__ parameter "value" cannot be nan.')

        self.value: object = value

        self.highlight: HighlightOutput = format['highlight'] if 'highlight' in format else HighlightOutput.REGULAR

        self.number_format: str = format['number_format'] if 'number_format' in format else ''

    def get_excel_format_properties(self):
        result = {}

        if self.highlight == HighlightOutput.REGULAR:
            pass
        elif self.highlight == HighlightOutput.WARNING:
            result['font_color'] = 'black'
            result['bg_color'] = 'yellow'
        elif self.highlight == HighlightOutput.ERROR:
            result['font_color'] = 'white'
            result['bg_color'] = 'red'
        elif self.highlight == HighlightOutput.GANTT_FILLER:
            result['font_color'] = 'white'
            result['bg_color'] = 'gray'

        if self.number_format:
            result['num_format'] = self.number_format

        return result

    def get_autofit_cell_width(self):
        if isinstance(self.value, str):
            return len(self.value)

        if isinstance(self.value, date):
            if self.number_format:
                return len(self.number_format)
            else:
                return 10

        if isinstance(self.value, float) or isinstance(self.value, int):
            if self.number_format == '0%':
                additional_symbol_because_percent_sign_is_very_wide_in_excel = 1
                return len('{:.0%}'.format(self.value)) + additional_symbol_because_percent_sign_is_very_wide_in_excel
            elif self.number_format == '# #0.0':
                return len('{:,.2f}'.format(self.value))

        return 0


