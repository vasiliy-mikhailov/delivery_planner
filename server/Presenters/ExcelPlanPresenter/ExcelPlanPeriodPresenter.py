from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelReport import ExcelReport
import datetime

class ExcelPlanPeriodPresenter:

    def __init__(self, start_date: datetime.date, end_date: datetime.date, report: ExcelReport):
        self.start_date: datetime.date = start_date
        self.end_date: datetime.date = end_date
        self.report: ExcelReport = report


    def present(self):
        page = self.report.add_page_named('Период расчета')
        page.write_cell(row=0, col=0, cell=ExcelCell(value='Начало'))
        start_date = self.start_date
        page.write_cell(row=0, col=1, cell=ExcelCell(value=start_date, format={'number_format': 'dd.mm.yyyy'}))
        page.write_cell(row=1, col=0, cell=ExcelCell(value='Окончание'))
        end_date = self.end_date
        page.write_cell(row=1, col=1, cell=ExcelCell(value=end_date, format={'number_format': 'dd.mm.yyyy'}))
        page.auto_fit_all_columns()
