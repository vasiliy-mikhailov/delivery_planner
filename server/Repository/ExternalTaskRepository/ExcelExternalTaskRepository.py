import math
from Entities.ExternalTask.ExternalTask import ExternalTask
import pandas as pd

from Entities.ExternalTask.ExternalTaskEffort import ExternalTaskEffort
from Entities.Skill.AbilityEnum import AbilityEnum


class ExcelExternalTaskRepository:
    def __init__(self, file_name_or_io):
        self.file_name_or_io = file_name_or_io
        self.task_data_frame = pd.read_excel(self.file_name_or_io, sheet_name=0)

    def excel_cell_contains_value(self, value) -> bool:
        if isinstance(value, float) and math.isnan(value):
            return False
        else:
            return True

    def append_efforts_if_greater_than_zero(self, external_task: ExternalTask, hours_value, ability: AbilityEnum):
        if self.excel_cell_contains_value(hours_value) and hours_value > 0:
            external_task.efforts.append(ExternalTaskEffort(ability=ability, hours=hours_value))

    def read_external_task_from_row_without_children(self, external_task_row) -> ExternalTask:
        id = external_task_row['ID']
        name = external_task_row['NAME'] if self.excel_cell_contains_value(external_task_row['NAME']) else ''
        system = external_task_row['SYSTEM'] if self.excel_cell_contains_value(external_task_row['SYSTEM']) else ''

        result = ExternalTask(
            id=id,
            name=name,
            system=system,
        )

        self.append_efforts_if_greater_than_zero(external_task=result, hours_value=external_task_row['SYSTEM_ANALYSIS_HOURS_LEFT'], ability=AbilityEnum.SYSTEM_ANALYSIS)
        self.append_efforts_if_greater_than_zero(external_task=result, hours_value=external_task_row['DEVELOPMENT_HOURS_LEFT'], ability=AbilityEnum.DEVELOPMENT)
        self.append_efforts_if_greater_than_zero(external_task=result, hours_value=external_task_row['SYSTEM_TESTING_HOURS_LEFT'], ability=AbilityEnum.SYSTEM_TESTING)

        return result

    def read_external_tasks_from_rows(self, external_task_rows, level: int) -> [ExternalTask]:
        result = []

        for index, external_task_row in external_task_rows.iterrows():
            external_task = self.read_external_task_from_row_without_children(external_task_row=external_task_row)

            result.append(external_task)

            if level < 3:
                task_data_frame = self.task_data_frame
                external_task_id = external_task_row['ID']
                sub_task_rows = task_data_frame.loc[task_data_frame['PARENT_ID'] == external_task_id]
                external_task.sub_tasks = self.read_external_tasks_from_rows(external_task_rows=sub_task_rows, level=level+1)

        return result

    def get_external_task_by_id(self, external_task_id: str) -> ExternalTask:
        task_data_frame = self.task_data_frame
        external_task_rows = task_data_frame.loc[task_data_frame['ID'] == external_task_id]

        if len(external_task_rows) == 1:
            return self.read_external_tasks_from_rows(external_task_rows=external_task_rows, level=1)[0]
        else:
            raise ValueError(
                'ExcelExternalTaskRepository get_external_task_by_id expected exactly 1 task with id {}, but {} found.'.format(
                    external_task_id, len(external_task_rows)))

    def has_external_task_with_id(self, external_task_id: str) -> bool:
        task_data_frame = self.task_data_frame
        external_task_rows = task_data_frame.loc[task_data_frame['ID'] == external_task_id]

        has_exactly_one_task_with_id = len(external_task_rows) == 1

        return has_exactly_one_task_with_id

    def get_all(self) -> [ExternalTask]:
        task_data_frame = self.task_data_frame
        first_level_external_task_rows = task_data_frame[task_data_frame['PARENT_ID'].isnull()]

        return self.read_external_tasks_from_rows(external_task_rows=first_level_external_task_rows, level=1)