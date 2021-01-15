from Entities.Skill.AbilityEnum import AbilityEnum
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceLackOutput import ResourceLackOutput
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelResourceLackPresenter:

    def __init__(self, plan_output: PlanOutput, report: ExcelReport):
        self.plan_output: PlanOutput = plan_output
        self.report: ExcelReport = report

    EXCEL_ABILITY_ENUM_TO_COLUMN_NAME_MAPPING = {
        AbilityEnum.SOLUTION_ARCHITECTURE: 'Архитектор решения (не хватает часов)',
        AbilityEnum.PROJECT_MANAGEMENT: 'Руководитель проекта (не хватает часов)',
        AbilityEnum.SYSTEM_ANALYSIS: 'Системный аналитик (не хватает часов)',
        AbilityEnum.DEVELOPMENT: 'Разработчик (не хватает часов)',
        AbilityEnum.SYSTEM_TESTING: 'Системный тестировщик (не хватает часов)',
        AbilityEnum.INTEGRATION_TESTING: 'Интеграционный тестировщик (не хватает часов)',
        AbilityEnum.PRODUCT_OWNERSHIP: 'Владелец продукта (не хватает часов)'
    }

    def present_resource_ability_names_header(self, page: ExcelPage, start_col: int):
        for i, ability in enumerate(AbilityEnum):
            col = start_col + i
            ability_name = self.EXCEL_ABILITY_ENUM_TO_COLUMN_NAME_MAPPING[ability]
            page.write_cell(row=0, col=col, cell=ExcelCell(value=ability_name))

    def present_resource_lacks_header(self, page: ExcelPage):
        page.write_cell(row=0, col=0, cell=ExcelCell(value='Бизнес-линия'))
        page.write_cell(row=0, col=1, cell=ExcelCell(value='Система'))
        self.present_resource_ability_names_header(page=page, start_col=2)

    def present_resource_ability_hours(self, page: ExcelPage, resource_lack: ResourceLackOutput, row: int, start_col: int):
        efforts = resource_lack.efforts

        for i, ability in enumerate(AbilityEnum):
            hours = sum([effort.hours for effort in efforts if effort.ability == ability])

            if hours:
                col = start_col + i
                page.write_cell(row=row, col=col, cell=ExcelCell(value=hours, format={'number_format': '# ##0.0'}))

    def present_resource_lacks_data(self, page: ExcelPage, start_row: int):
        resource_lacks = self.plan_output.resource_lacks

        for i, resource_lack in enumerate(resource_lacks):
            row = start_row + i
            business_line = resource_lack.business_line
            system = resource_lack.system
            page.write_cell(row=row, col=0, cell=ExcelCell(value=business_line))
            page.write_cell(row=row, col=1, cell=ExcelCell(value=system))
            self.present_resource_ability_hours(page=page, resource_lack=resource_lack, row=row, start_col=2)

    def present_resource_lacks(self, page: ExcelPage):
        self.present_resource_lacks_header(page=page)
        self.present_resource_lacks_data(page=page, start_row=1)

    def present(self):
        page = self.report.add_page_named('out_Недостаток ресурсов')

        self.present_resource_lacks(page=page)
        page.auto_fit_column(0)
        page.auto_fit_column(1)