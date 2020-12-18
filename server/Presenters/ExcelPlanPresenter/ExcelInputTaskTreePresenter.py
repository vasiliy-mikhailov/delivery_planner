from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.TaskOutput import TaskOutput
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelInputTaskTreePresenter:


    def __init__(self, tasks: [TaskOutput], report: ExcelReport):
        self.tasks: [TaskOutput] = tasks
        self.report: ExcelReport = report


    EXCEL_ABILITY_ENUM_TO_COLUMN_NAME_MAPPING = {
        AbilityEnum.SOLUTION_ARCHITECTURE: 'Архитектор решения (осталось часов)',
        AbilityEnum.PROJECT_MANAGEMENT: 'Руководитель проекта (осталось часов)',
        AbilityEnum.SYSTEM_ANALYSIS: 'Системный аналитик (осталось часов)',
        AbilityEnum.DEVELOPMENT: 'Разработчик (осталось часов)',
        AbilityEnum.SYSTEM_TESTING: 'Системный тестировщик (осталось часов)',
        AbilityEnum.INTEGRATION_TESTING: 'Интеграционный тестировщик (осталось часов)',
        AbilityEnum.PRODUCT_OWNERSHIP: 'Владелец продукта (осталось часов)'
    }

    EXCEL_ABILITY_ENUM_TO_TEAM_MEMBER_ABILITY_MAPPING = {
        AbilityEnum.SOLUTION_ARCHITECTURE: 'Архитектура решения',
        AbilityEnum.PROJECT_MANAGEMENT: 'Управление проектом',
        AbilityEnum.SYSTEM_ANALYSIS: 'Системная аналитика',
        AbilityEnum.DEVELOPMENT: 'Разработка',
        AbilityEnum.SYSTEM_TESTING: 'Системное тестирование',
        AbilityEnum.INTEGRATION_TESTING: 'Интеграционное тестирование',
        AbilityEnum.PRODUCT_OWNERSHIP: 'Управление продуктом'
    }

    def present_hours_left_header(self, start_col: int, page: ExcelPage):
        for i, ability in enumerate(AbilityEnum):
            column_name = self.EXCEL_ABILITY_ENUM_TO_COLUMN_NAME_MAPPING[ability]
            page.write_cell(row=0, col=start_col + i, cell=ExcelCell(value=column_name))


    def present_header(self, page: ExcelPage):
        page.write_cell(row=0, col=0, cell=ExcelCell(value='id'))
        page.write_cell(row=0, col=1, cell=ExcelCell(value='Бизнес-линия'))
        page.write_cell(row=0, col=2, cell=ExcelCell(value='Заявка на доработку ПО'))
        page.write_cell(row=0, col=3, cell=ExcelCell(value='Заявка на доработку системы'))
        page.write_cell(row=0, col=4, cell=ExcelCell(value='Подзадача'))
        page.write_cell(row=0, col=5, cell=ExcelCell(value='Предшественники'))
        page.write_cell(row=0, col=6, cell=ExcelCell(value='Система'))
        page.write_cell(row=0, col=7, cell=ExcelCell(value='Работа'))
        page.write_cell(row=0, col=8, cell=ExcelCell(value='Количество или id ресурса'))
        self.present_hours_left_header(start_col=9, page=page)


    def present_hours_left(self, task_output: TaskOutput, row: int, start_col: int, page: ExcelPage):
        effort = task_output.efforts
        for i, ability in enumerate(AbilityEnum):
            hours = sum([e.hours for e in effort if e.ability == ability])

            if hours:
                page.write_cell(row=row, col=start_col + i, cell=ExcelCell(value=hours, format={'number_format': '# ##0.0'}))

    def present_team_members(self, task_output: TaskOutput, start_row: int, page: ExcelPage):
        row = start_row
        team_members = task_output.team_members

        for team_member in team_members:
            ability = team_member.ability
            ability_description = self.EXCEL_ABILITY_ENUM_TO_TEAM_MEMBER_ABILITY_MAPPING[ability]
            resource_ids_and_or_quantities = team_member.resource_ids_and_or_quantities

            for resource_id_and_or_quantity in resource_ids_and_or_quantities:
                page.write_cell(row=row, col=7, cell=ExcelCell(value=ability_description))
                page.write_cell(row=row, col=8, cell=ExcelCell(value=resource_id_and_or_quantity))
                page.collapse_row(row=row, level=3)
                row = row + 1

        return row


    def present_predecessors(self, predecessors: [TaskOutput], row: int, col: int, page: ExcelPage):
        predecessors_str = ";".join([predecessor.id for predecessor in predecessors])
        page.write_cell(row=row, col=col, cell=ExcelCell(value=predecessors_str))


    def present_task_recursive_and_return_row(self, task_output: TaskOutput, start_row: int, level: int, page: ExcelPage):
        row = start_row
        page.write_cell(row=row, col=0, cell=ExcelCell(value=task_output.id))
        page.write_cell(row=row, col=1, cell=ExcelCell(value=task_output.business_line))
        page.write_cell(row=row, col=2 + level, cell=ExcelCell(value=task_output.name))
        self.present_predecessors(predecessors=task_output.predecessors, row=row, col=5, page=page)
        page.write_cell(row=row, col=6, cell=ExcelCell(value=task_output.system))

        self.present_hours_left(task_output=task_output, row=row, start_col=9, page=page)
        if level > 0:
            page.collapse_row(row=row, level=level)

        row = row + 1

        row = self.present_team_members(task_output=task_output, start_row=row, page=page)

        row = self.present_tasks_recursive_and_return_row(task_outputs=task_output.sub_tasks, start_row=row, level=level+1, page=page)
        return row


    def present_tasks_recursive_and_return_row(self, task_outputs: [TaskOutput], start_row: int, level: int, page: ExcelPage):
        row = start_row
        for task in task_outputs:
            row = self.present_task_recursive_and_return_row(task_output=task, start_row=row, level=level, page=page)

        return row


    def present(self):
        page = self.report.add_page_named('Заявки')
        self.present_header(page=page)
        tasks = self.tasks
        self.present_tasks_recursive_and_return_row(task_outputs=tasks, start_row=1, level=0, page=page)
        page.auto_fit_column(col=0)
        page.auto_fit_column(col=1)
        page.set_column_width(col=4, width=70)
        page.auto_fit_column(col=6)
        page.auto_fit_column(col=7)
        page.auto_fit_column(col=8)
