from xlsxwriter.worksheet import Worksheet
from Presenters.ExcelWrapper.ExcelCell import ExcelCell

class ExcelPage:

    def __init__(self, worksheet: Worksheet, parent_report: object):
        self.worksheet: Worksheet = worksheet
        self.cols: {} = {}
        self.parent_report: object = parent_report
        self.collapse_level_by_row = {}
        self.frozen_row_and_column = None
        self.hints: {} = {}

    def get_name(self):
        return self.worksheet.get_name()

    def write_cell_to_excel_workbook(self, row: int, col: int, cell: ExcelCell):
        format_properties = cell.get_excel_format_properties()
        cell_format = self.parent_report.add_format(format_properties)
        self.worksheet.write(row, col, cell.value, cell_format)

    def store_cell_in_memory(self, row: int, col: int, cell: ExcelCell):
        if col not in self.cols:
            self.cols[col] = {}

        rows = self.cols[col]

        rows[row] = cell

    def write_cell(self, row: int, col: int, cell: ExcelCell):
        self.write_cell_to_excel_workbook(row, col, cell)

        self.store_cell_in_memory(row, col, cell)

    def read_cell(self, row: int, col: int):
        return self.cols[col][row]

    def get_auto_fit_column_width(self, col: int):
        row = self.cols[col]

        result = 0

        for cell in row.values():
            cell_width = cell.get_autofit_cell_width()
            result = max(cell_width, result)

        return result

    def set_column_width(self, col: int, width: int):
        self.worksheet.set_column(col, col, width=width)

    def auto_fit_column(self, col: int):
        width = self.get_auto_fit_column_width(col=col)
        self.set_column_width(col=col, width=width)

    def auto_fit_all_columns(self):
        for col in self.cols.keys():
            self.auto_fit_column(col)

    def collapse_row(self, row: int, level: int):
        self.worksheet.set_row(row, None, None, {'hidden': 1, 'collapsed': 1, 'level': level})
        self.collapse_level_by_row[row] = level

    def get_collapse_level_for_row(self, row: int) -> int:
        if row in self.collapse_level_by_row:
            return self.collapse_level_by_row[row]
        else:
            return 0

    def freeze_row_and_column(self, top_row: int, left_column: int):
        self.worksheet.freeze_panes(row=top_row, col=left_column)
        self.frozen_row_and_column = (top_row, left_column)

    def get_frozen_row_and_column(self):
        if self.frozen_row_and_column:
            return self.frozen_row_and_column
        else:
            raise ValueError

    def set_hint_for_row_and_col(self, row: int, col: int, hint: str):
        self.hints[(row, col)] = hint
        self.worksheet.write_comment(row=row, col=col, comment=hint, options={'font_size': 12, 'width': 600})

    def get_hint_for_row_and_col(self, row: int, col: int) -> str:
        return self.hints[(row, col)]