import math

from Repository.ExternalTaskReader.ExternalTaskRowsReader import ExternalTaskRowsReader
import pandas as pd

class FlatFileExternalTaskRowsReader(ExternalTaskRowsReader):
    def __init__(self, file_name: str):
        self.file_name: str = file_name

    def excel_cell_contains_value(self, value) -> bool:
        if isinstance(value, float) and math.isnan(value):
            return False
        else:
            return True

    def read_task_rows(self) -> [{}]:
        task_rows = []
        tasks_sheet = pd.read_excel(self.file_name, sheet_name=0)
        for index, row in tasks_sheet.iterrows():
            task_row = {}
            task_row['id'] = row['ID']

            task_row['name'] = row['NAME'] if self.excel_cell_contains_value(row['NAME']) else ''
            task_row['system'] = row['SYSTEM'] if self.excel_cell_contains_value(row['SYSTEM']) else ''

            if self.excel_cell_contains_value(row['SYSTEM_ANALYSIS_HOURS_LEFT']) and row['SYSTEM_ANALYSIS_HOURS_LEFT'] > 0:
                task_row['system_analysis_hours_left'] = row['SYSTEM_ANALYSIS_HOURS_LEFT']

            if self.excel_cell_contains_value(row['DEVELOPMENT_HOURS_LEFT']) and row['DEVELOPMENT_HOURS_LEFT'] > 0:
                task_row['development_hours_left'] = row['DEVELOPMENT_HOURS_LEFT']

            if self.excel_cell_contains_value(row['SYSTEM_TESTING_HOURS_LEFT']) and row['SYSTEM_TESTING_HOURS_LEFT'] > 0:
                task_row['system_testing_hours_left'] = row['SYSTEM_TESTING_HOURS_LEFT']

            if self.excel_cell_contains_value(row['PARENT_ID']):
                task_row['parent_id'] = row['PARENT_ID']

            task_rows.append(task_row)

        return task_rows

    def read(self) -> [{}]:
        result = self.read_task_rows()
        return result