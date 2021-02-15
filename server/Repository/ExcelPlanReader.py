import math
from Inputs.PlanInput import PlanInput
import pandas as pd

from Inputs.TaskIdInput import TaskIdInput
from Inputs.TaskInput import TaskInput
from Inputs.EffortInput import EffortInput
from Entities.Skill.AbilityEnum import AbilityEnum
from Inputs.CapacityInput import CapacityInput
from Inputs.ExistingResourceInput import ExistingResourceInput
from Inputs.PlannedResourceInput import PlannedResourceInput
from Inputs.TeamMemberInput import TeamMemberInput
from Inputs.TemporaryResourceInput import TemporaryResourceInput
from Inputs.VacationInput import VacationInput


class ExcelPlanReader:
    EXCEL_EFFORT_ABILITY_TO_ABILITY_ENUM_MAPPING = {
        'Архитектор решения (осталось часов)': AbilityEnum.SOLUTION_ARCHITECTURE,
        'Руководитель проекта (осталось часов)': AbilityEnum.PROJECT_MANAGEMENT,
        'Системный аналитик (осталось часов)': AbilityEnum.SYSTEM_ANALYSIS,
        'Разработчик (осталось часов)': AbilityEnum.DEVELOPMENT,
        'Системный тестировщик (осталось часов)': AbilityEnum.SYSTEM_TESTING,
        'Интеграционный тестировщик (осталось часов)': AbilityEnum.INTEGRATION_TESTING,
        'Владелец продукта (осталось часов)': AbilityEnum.PRODUCT_OWNERSHIP
    }

    EXCEL_RESOURCE_ABILITY_TO_ABILITY_ENUM_MAPPING = {
        'Архитектор решения': AbilityEnum.SOLUTION_ARCHITECTURE,
        'Руководитель проекта': AbilityEnum.PROJECT_MANAGEMENT,
        'Системный аналитик': AbilityEnum.SYSTEM_ANALYSIS,
        'Разработчик': AbilityEnum.DEVELOPMENT,
        'Системный тестировщик': AbilityEnum.SYSTEM_TESTING,
        'Интеграционный тестировщик': AbilityEnum.INTEGRATION_TESTING,
        'Владелец продукта': AbilityEnum.PRODUCT_OWNERSHIP
    }

    EXCEL_TEAM_MEMBER_ABILITY_TO_ABILITY_ENUM_MAPPING = {
        'Архитектура решения': AbilityEnum.SOLUTION_ARCHITECTURE,
        'Управление проектом': AbilityEnum.PROJECT_MANAGEMENT,
        'Системная аналитика': AbilityEnum.SYSTEM_ANALYSIS,
        'Разработка': AbilityEnum.DEVELOPMENT,
        'Системное тестирование': AbilityEnum.SYSTEM_TESTING,
        'Интеграционное тестирование': AbilityEnum.INTEGRATION_TESTING,
        'Управление продуктом': AbilityEnum.PRODUCT_OWNERSHIP
    }

    def __init__(self, file_name_or_io: str):
        self.file_name_or_io: str = file_name_or_io
        self.file_data_cache: {} = pd.read_excel(file_name_or_io, sheet_name=None)

    def sheet_exists(self, sheet_name: str):
        file_data_cache = self.file_data_cache
        return sheet_name in file_data_cache

    def read_task_ids_to_add_from_sheet(self, sheet_name: str):
        result = []
        file_data_cache = self.file_data_cache
        task_ids_to_add_sheet = file_data_cache[sheet_name]
        for index, row in task_ids_to_add_sheet.iterrows():
            task_id = row['id']
            task_id_input = TaskIdInput(id=task_id)
            result.append(task_id_input)

        return result

    def read_task_ids_to_add(self):
        sheet_name = 'Добавить заявки по id'
        if self.sheet_exists(sheet_name=sheet_name):
            return self.read_task_ids_to_add_from_sheet(sheet_name=sheet_name)
        else:
            return []

    def read_plan_dates(self):
        file_data_cache = self.file_data_cache
        period_sheet = file_data_cache['Период расчета']
        dates = period_sheet['Значение'].tolist()
        start = dates[0].date()
        end = dates[1].date()
        return start, end

    def read_hours_from_row(self, row, column: str, ability: AbilityEnum):
        hours: float = float(row[column])
        return EffortInput(ability=ability, hours=hours)

    def excel_cell_contains_value(self, value) -> bool:
        if isinstance(value, float) and math.isnan(value):
            return False
        else:
            return True

    def read_effort_from_row(self, row):
        result = []
        for ability_name in self.EXCEL_EFFORT_ABILITY_TO_ABILITY_ENUM_MAPPING.keys():
            hours = row[ability_name]
            if self.excel_cell_contains_value(hours) and hours > 0:
                ability = self.EXCEL_EFFORT_ABILITY_TO_ABILITY_ENUM_MAPPING[ability_name]
                effort = EffortInput(ability=ability, hours=hours)
                result.append(effort)
        return result

    def read_task_from_row(self, row, task_name_col: str):
        id: str = row['id']
        name: str = row[task_name_col]
        system: str = row['Система']
        if not self.excel_cell_contains_value(system):
            system = ''

        business_line: str = row['Бизнес-линия']

        task = TaskInput(
            id=id,
            name=name,
            system=system,
            business_line=business_line,
        )

        task.efforts = self.read_effort_from_row(row)
        return task

    def append_task_to_list_of_level(self, task: TaskInput, task_list: [], level: int):
        if level == 1:
            task_list.append(task)
        else:
            last_task_in_list = task_list[len(task_list) - 1]
            self.append_task_to_list_of_level(task, last_task_in_list.sub_tasks, level - 1)

    def find_last_task(self, tasks: [TaskInput]):
        if len(tasks) > 0:
            last_task_on_this_level = tasks[len(tasks) - 1]

            has_next_level = len(last_task_on_this_level.sub_tasks) > 0
            if has_next_level:
                return self.find_last_task(last_task_on_this_level.sub_tasks)
            else:
                return last_task_on_this_level
        else:
            raise ValueError


    def read_tasks_and_team_members(self):
        tasks = []

        file_data_cache = self.file_data_cache
        tasks_sheet = file_data_cache['Заявки']
        for index, row in tasks_sheet.iterrows():
            if self.excel_cell_contains_value(value=row['Заявка на доработку ПО']):
                task = self.read_task_from_row(row=row, task_name_col='Заявка на доработку ПО')
                self.append_task_to_list_of_level(task=task, task_list=tasks, level=1)
            elif self.excel_cell_contains_value(value=row['Заявка на доработку системы']):
                task = self.read_task_from_row(row=row, task_name_col='Заявка на доработку системы')
                self.append_task_to_list_of_level(task=task, task_list=tasks, level=2)
            elif self.excel_cell_contains_value(value=row['Подзадача']):
                task = self.read_task_from_row(row=row, task_name_col='Подзадача')
                self.append_task_to_list_of_level(task=task, task_list=tasks, level=3)
            elif self.excel_cell_contains_value(value=row['Работа']):
                task = self.find_last_task(tasks=tasks)
                system = task.system
                ability = self.EXCEL_TEAM_MEMBER_ABILITY_TO_ABILITY_ENUM_MAPPING[row['Работа']]
                resource_ids_and_or_quantity_split_by_semicolon_line_str = str(row['Количество или id ресурса'])
                resource_ids_and_or_quantity_split_by_semicolon_line = str(resource_ids_and_or_quantity_split_by_semicolon_line_str).split(';')
                team_member_input = TeamMemberInput(
                        system=system,
                        ability=ability,
                        resource_ids_and_or_quantities=resource_ids_and_or_quantity_split_by_semicolon_line
                )
                task.team_members.append(team_member_input)

        return tasks

    def find_tasks_by_id_recursive(self, task_id: str, tasks: [TaskInput]):
        result = []

        for task in tasks:
            if task.id == task_id:
                result.append(task)

            task_children_with_desired_task_id = self.find_tasks_by_id_recursive(task_id=task_id, tasks=task.sub_tasks)

            result = result + task_children_with_desired_task_id

        return result

    def find_task_by_id(self, task_id: str, tasks: [TaskInput]) -> TaskInput:
        found_tasks = self.find_tasks_by_id_recursive(task_id=task_id, tasks=tasks)

        if (len(found_tasks) == 1):
            return found_tasks[0]
        else:
            raise ValueError('Must be exactly one task with id "{}", but {} found'.format(task_id, len(found_tasks)))

    def fill_predecessors(self, task_id: str, predecessor_ids: [str], tasks: [TaskInput]):
        task_input = self.find_task_by_id(task_id, tasks=tasks)

        predecessors = [self.find_task_by_id(id, tasks=tasks) for id in predecessor_ids]

        task_input.predecessors = predecessors

    def read_predecessors(self, tasks: [TaskInput]):
        result = []

        file_data_cache = self.file_data_cache
        tasks_sheet = file_data_cache['Заявки']
        for index, row in tasks_sheet.iterrows():
            task_id = row['id']
            predecessor_ids = row['Предшественники']

            if self.excel_cell_contains_value(task_id) and self.excel_cell_contains_value(predecessor_ids):
                predecessor_ids_list = predecessor_ids.split(';')
                self.fill_predecessors(task_id=task_id, predecessor_ids=predecessor_ids_list, tasks=tasks)

        return result

    def read_resource_capacity_from_column(self, row, column: str):
        hours: float = float(row[column])
        ability = self.EXCEL_RESOURCE_ABILITY_TO_ABILITY_ENUM_MAPPING[column]
        system = row['Система']
        return CapacityInput(system=system, ability=ability, efficiency=hours)

    def read_resource_capacities_from_row(self, row):
        result = []
        for ability_name in self.EXCEL_RESOURCE_ABILITY_TO_ABILITY_ENUM_MAPPING.keys():
            if row[ability_name]:
                resource_capacity = self.read_resource_capacity_from_column(row, ability_name)
                result.append(resource_capacity)
        return result

    def read_vacations(self):
        result = []

        file_data_cache = self.file_data_cache
        vacations_sheet = file_data_cache['Отпуска']
        for index, row in vacations_sheet.iterrows():
            if row['id ресурса']:
                resource_id = row['id ресурса']
                start_date = row['с']
                end_date = row['по']
                vacation = VacationInput(resource_id=resource_id, start_date=start_date, end_date=end_date)
                result.append(vacation)

        return result

    def read_existing_resources(self):
        result = []

        file_data_cache = self.file_data_cache
        existing_resources_sheet = file_data_cache['Существующие ресурсы']
        existing_resources_sheet = existing_resources_sheet.fillna('')
        for index, row in existing_resources_sheet.iterrows():
            if row['id']:
                existing_resource = ExistingResourceInput(
                    id=row['id'],
                    name=row['ФИО'],
                    business_line=row['Бизнес-линия'],
                    calendar=row['Календарь'],
                    hours_per_day=float(row['Часов на новый функционал в день'])
                )
                result.append(existing_resource)

            last_resource = result[-1]
            last_resource.capacity_per_day = last_resource.capacity_per_day + self.read_resource_capacities_from_row(
                row)
        return result

    def read_planned_resources(self):
        result = []

        file_data_cache = self.file_data_cache
        planned_resources_sheet = file_data_cache['Планируемые ресурсы']
        planned_resources_sheet = planned_resources_sheet.fillna('')
        for index, row in planned_resources_sheet.iterrows():
            planned_resource = PlannedResourceInput(
                id=row['id'],
                name=row['Название'],
                business_line=row['Бизнес-линия'],
                start_date=row['Дата появления'].date(),
                full_power_in_month=float(row['Время до выхода на полную мощность (месяцев)']),
                calendar=row['Календарь'],
                hours_per_day=float(row['Часов на новый функционал в день'])
            )
            result.append(planned_resource)

            last_resource = result[-1]
            last_resource.capacity_per_day = last_resource.capacity_per_day + self.read_resource_capacities_from_row(
                row)
        return result

    def read_temporary_resources(self):
        result = []

        file_data_cache = self.file_data_cache
        temporary_resources_sheet = file_data_cache['Временные ресурсы']
        temporary_resources_sheet = temporary_resources_sheet.fillna('')
        for index, row in temporary_resources_sheet.iterrows():
            start_date_value = row['Первый рабочий день (необязательно)']
            if start_date_value:
                has_start_date = True
                start_date = start_date_value.date()
            else:
                has_start_date = False
                start_date = None

            end_date_value = row['Последний рабочий день (необязательно)']
            if end_date_value:
                has_end_date = True
                end_date = end_date_value.date()
            else:
                has_end_date = False
                end_date = None

            temporary_resource = TemporaryResourceInput(
                id=row['id'],
                name=row['Название'],
                business_line=row['Бизнес-линия'],
                has_start_date=has_start_date,
                start_date=start_date,
                has_end_date=has_end_date,
                end_date=end_date,
                calendar=row['Календарь'],
                hours_per_day=float(row['Часов на новый функционал в день'])
            )
            result.append(temporary_resource)

            last_resource = result[-1]
            last_resource.capacity_per_day = last_resource.capacity_per_day + self.read_resource_capacities_from_row(
                row)
        return result

    def read(self) -> PlanInput:
        start, end = self.read_plan_dates()
        result = PlanInput(start_date=start, end_date=end)
        result.task_ids_to_add = self.read_task_ids_to_add()
        result.existing_resources = self.read_existing_resources()
        result.vacations = self.read_vacations()
        result.planned_resources = self.read_planned_resources()
        result.temporary_resources = self.read_temporary_resources()
        result.tasks = self.read_tasks_and_team_members()
        self.read_predecessors(tasks=result.tasks)
        return result
