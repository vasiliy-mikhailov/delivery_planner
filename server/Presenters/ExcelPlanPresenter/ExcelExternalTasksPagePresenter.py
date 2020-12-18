from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.ExternalTaskOutput import ExternalTaskOutput
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelExternalTasksPagePresenter:
    def __init__(self, external_tasks: [ExternalTaskOutput], report: ExcelReport):
        self.external_tasks: [ExternalTaskOutput] = external_tasks
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
        page.write_cell(row=0, col=5, cell=ExcelCell(value='Система'))
        self.present_hours_left_header(start_col=6, page=page)


    def present_hours_left(self, external_task: ExternalTaskOutput, row: int, start_col: int, page: ExcelPage):
        effort = external_task.efforts
        for i, ability in enumerate(AbilityEnum):
            hours = sum([e.hours for e in effort if e.ability == ability])

            if hours:
                page.write_cell(row=row, col=start_col + i, cell=ExcelCell(value=hours, format={'number_format': '# ##0.0'}))


    def present_external_task_recursive_and_return_row(self, external_tasks: ExternalTaskOutput, start_row: int, level: int, page: ExcelPage):
        row = start_row
        page.write_cell(row=row, col=0, cell=ExcelCell(value=external_tasks.id))
        page.write_cell(row=row, col=1, cell=ExcelCell(value=external_tasks.business_line))
        page.write_cell(row=row, col=2 + level, cell=ExcelCell(value=external_tasks.name))
        page.write_cell(row=row, col=5, cell=ExcelCell(value=external_tasks.system))

        self.present_hours_left(external_task=external_tasks, row=row, start_col=6, page=page)
        if level > 0:
            page.collapse_row(row=row, level=level)

        row = row + 1

        row = self.present_external_tasks_recursive_and_return_row(external_tasks=external_tasks.sub_tasks, start_row=row, level=level + 1, page=page)
        return row


    def present_external_tasks_recursive_and_return_row(self, external_tasks: [ExternalTaskOutput], start_row: int, level: int, page: ExcelPage):
        row = start_row
        for task in external_tasks:
            row = self.present_external_task_recursive_and_return_row(external_tasks=task, start_row=row, level=level, page=page)

        return row


    def present(self):
        page = self.report.add_page_named('Репозиторий задач')
        self.present_header(page=page)
        external_tasks = self.external_tasks
        self.present_external_tasks_recursive_and_return_row(external_tasks=external_tasks, start_row=1, level=0, page=page)
        page.auto_fit_column(col=0)
        page.auto_fit_column(col=1)
        page.set_column_width(col=4, width=70)
        page.auto_fit_column(col=5)
