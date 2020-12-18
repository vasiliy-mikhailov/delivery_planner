from Outputs.TaskResourceSupplyOutputs.TaskResourceSupplyRowOutput import \
    TaskResourceSupplyRowOutput
from Outputs.PlanOutput import PlanOutput
from Presenters.ExcelWrapper.ExcelAbilityFormatter import ExcelAbilityFormatter
from Presenters.ExcelWrapper.ExcelBooleanFormatter import ExcelBooleanFormatter
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelTaskResourceSupplyPresenter:

    def __init__(self, plan_output: PlanOutput, report: ExcelReport):
        self.plan_output: PlanOutput = plan_output
        self.report: ExcelReport = report

    def present_task_data(self, start_row: int, start_col: int, page: ExcelPage):
        page.write_cell(row=start_row + 0, col=start_col + 0, cell=ExcelCell(value='id заявки'))
        page.write_cell(row=start_row + 0, col=start_col + 1, cell=ExcelCell(value='Название'))
        page.write_cell(row=start_row + 0, col=start_col + 2, cell=ExcelCell(value='Бизнес-линия'))
        page.write_cell(row=start_row + 0, col=start_col + 3, cell=ExcelCell(value='Хватает ресурсов?'))

        excel_boolean_formatter = ExcelBooleanFormatter()

        for i, row in enumerate(self.plan_output.task_resource_supply.rows):
            page.write_cell(row=2 + i, col=0, cell=ExcelCell(value=row.task_id))
            page.write_cell(row=2 + i, col=1, cell=ExcelCell(value=row.task_name))
            page.write_cell(row=2 + i, col=2, cell=ExcelCell(value=row.business_line))
            page.write_cell(row=2 + i, col=3, cell=ExcelCell(value=excel_boolean_formatter.format(row.is_fully_supplied), format={'highlight': row.is_fully_supplied_highlight}))

    def generate_column_numbers_for_skills(self, rows: TaskResourceSupplyRowOutput):
        skill_column_number = {}

        for row in rows:
            for skill_resource_supply in row.skill_resource_supply:
                ability = skill_resource_supply.ability
                if ability not in skill_column_number:
                    skill_column_number[ability] = {}

                system = skill_resource_supply.system

                if system not in skill_column_number[ability]:
                    skill_column_number[ability][system] = None

        column_number = 0

        result = {}

        for ability in sorted(skill_column_number.keys(), key=lambda x: x.value):
            result[ability] = {}
            for system in sorted(skill_column_number[ability].keys()):
                result[ability][system] = column_number
                column_number = column_number + 1

        return result

    def present_skills_header(self, start_row: int, start_col: int, page: ExcelPage, skill_column_numbers):
        excel_ability_formatter = ExcelAbilityFormatter()

        for ability in skill_column_numbers.keys():
            systems = skill_column_numbers[ability]
            first_system = next(iter(systems))
            ability_column_number = skill_column_numbers[ability][first_system]
            page.write_cell(row=start_row + 0, col=start_col + ability_column_number, cell=ExcelCell(value=excel_ability_formatter.format(ability)))

            for system in systems.keys():
                column_number = skill_column_numbers[ability][system]
                page.write_cell(row=start_row + 1, col=start_col + column_number, cell=ExcelCell(value=system))

    def present_skills_data(self, start_row: int, start_col: int, page: ExcelPage, rows: [TaskResourceSupplyRowOutput], skill_column_numbers):
        for r, row in enumerate(rows):
            for supply in row.skill_resource_supply:
                system = supply.system
                ability = supply.ability
                supply_percent = supply.supply_percent
                highlight = supply.highlight
                column_number = skill_column_numbers[ability][system]
                page.write_cell(row=start_row + r, col=start_col + column_number, cell=ExcelCell(value=supply_percent, format={'highlight': highlight, 'number_format': '0%'}))

    def present_skills(self, start_row: int, start_col: int, page: ExcelPage):
        rows = self.plan_output.task_resource_supply.rows
        skill_column_numbers = self.generate_column_numbers_for_skills(rows)
        self.present_skills_header(start_row=start_row + 0, start_col=start_col, page=page, skill_column_numbers=skill_column_numbers)
        self.present_skills_data(start_row=start_row + 2, start_col=start_col, page=page, rows=rows, skill_column_numbers=skill_column_numbers)


    def present(self):
        page = self.report.add_page_named('out_Обеспеченность ресурсами')

        self.present_task_data(start_row=0, start_col=0, page=page)
        self.present_skills(start_row=0, start_col=4, page=page)
        page.freeze_row_and_column(top_row=2, left_column=5)
        page.auto_fit_column(0)
        page.auto_fit_column(1)
        page.auto_fit_column(2)
        page.auto_fit_column(3)
        page.auto_fit_column(4)