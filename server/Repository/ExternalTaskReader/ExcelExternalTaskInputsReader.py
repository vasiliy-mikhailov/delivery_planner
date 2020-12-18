import math

import pandas as pd
from Inputs.ExternalTaskInput import ExternalTaskInput
from Repository.ExternalTaskReader.ExternalTaskRowsReader import ExternalTaskRowsReader


class ExcelExternalTaskRowsReader(ExternalTaskRowsReader):
    EXCEL_EFFORT_ABILITY_TO_TASK_ROW_ABILITY_MAPPING = {
        'Архитектор решения (осталось часов)': 'solution_architecture_hours_left',
        'Руководитель проекта (осталось часов)': 'project_management_hours_left',
        'Системный аналитик (осталось часов)': 'system_analysis_hours_left',
        'Разработчик (осталось часов)': 'development_hours_left',
        'Системный тестировщик (осталось часов)': 'system_testing_hours_left',
        'Интеграционный тестировщик (осталось часов)': 'integration_testing_hours_left',
        'Владелец продукта (осталось часов)': 'product_ownership_hours_left'
    }

    def __init__(self, file_name: str):
        self.file_name: str = file_name

    def excel_cell_contains_value(self, value) -> bool:
        if isinstance(value, float) and math.isnan(value):
            return False
        else:
            return True

    def read_efforts_from_row(self, row):
        result = {}
        for excel_ability_name in self.EXCEL_EFFORT_ABILITY_TO_TASK_ROW_ABILITY_MAPPING.keys():
            hours = row[excel_ability_name]
            if self.excel_cell_contains_value(hours) and hours > 0:
                ability_name_task_row = self.EXCEL_EFFORT_ABILITY_TO_TASK_ROW_ABILITY_MAPPING[excel_ability_name]
                result[ability_name_task_row] = hours

        return result

    def read_task_row_from_row(self, row, task_name_col: str):
        id: str = row['id']
        name: str = row[task_name_col]
        system: str = row['Система']
        if not self.excel_cell_contains_value(system):
            system = ''

        business_line: str = row['Бизнес-линия']

        task = {
            'id': id,
            'name': name,
            'system': system,
            'business_line': business_line,
        }

        efforts = self.read_efforts_from_row(row)

        task = {**task, **efforts}

        return task

    def append_task_to_list_of_level(self, task: ExternalTaskInput, task_list: [], level: int):
        if level == 1:
            task_list.append(task)
        else:
            last_task_in_list = task_list[len(task_list) - 1]
            self.append_task_to_list_of_level(task, last_task_in_list.sub_tasks, level - 1)

    def read_task_rows(self) -> [{}]:
        task_rows = []
        tasks_sheet = pd.read_excel(self.file_name, sheet_name='Репозиторий задач')
        for index, row in tasks_sheet.iterrows():
            if self.excel_cell_contains_value(value=row['Заявка на доработку ПО']):
                task_row = self.read_task_row_from_row(row=row, task_name_col='Заявка на доработку ПО')
                task_rows.append(task_row)
                last_id_of_level_1 = task_row['id']
            elif self.excel_cell_contains_value(value=row['Заявка на доработку системы']):
                task_row = self.read_task_row_from_row(row=row, task_name_col='Заявка на доработку системы')
                task_row['parent_id'] = last_id_of_level_1
                task_rows.append(task_row)
                last_id_of_level_2 = task_row['id']
            elif self.excel_cell_contains_value(value=row['Подзадача']):
                task_row = self.read_task_row_from_row(row=row, task_name_col='Подзадача')
                task_row['parent_id'] = last_id_of_level_2
                task_rows.append(task_row)

        return task_rows

    def read(self) -> [{}]:
        result = self.read_task_rows()
        return result