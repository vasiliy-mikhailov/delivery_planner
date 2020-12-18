from Entities.Resource.Calendar.Calendar import generate_date_range
from Outputs.HightlightOutput import HighlightOutput
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanMemberOutput import ResourceCalendarPlanMemberOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationResourceOutput import ResourceUtilizationResourceOutput
from Outputs.ResourceUtilizationOutputs.ResourceUtilizationTaskOutput import ResourceUtilizationTaskOutput
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelResourceUtilizationPlanPresenter:
    def __init__(self, plan_output: PlanOutput, report: ExcelReport):
        self.plan_output: PlanOutput = plan_output
        self.report: ExcelReport = report


    def present_resource_utilization_plan_dates_header(self, start_row: int, start_column: int, page: ExcelPage):
        for i, date in enumerate(generate_date_range(self.plan_output.start_date, self.plan_output.end_date)):
            page.write_cell(row=start_row, col=start_column + i, cell=ExcelCell(value=date, format={'number_format': 'DD.MM'}))

    def present_resources_utilization_percent(self, row: int, start_column: int, resource: ResourceUtilizationResourceOutput, page: ExcelPage):
        resource_utilization_by_date = resource.utilization_by_date
        for i, date in enumerate(generate_date_range(self.plan_output.start_date, self.plan_output.end_date)):
            if date in resource_utilization_by_date:
                utilization_percent_output = resource_utilization_by_date[date]
                hours_spent = utilization_percent_output.value
                highlight = utilization_percent_output.highlight
                page.write_cell(row=row, col=start_column + i, cell=ExcelCell(value=hours_spent, format={'highlight': highlight, 'number_format': '0%'}))
            else:
                page.write_cell(row=row, col=start_column + i, cell=ExcelCell(value=0, format={'highlight': HighlightOutput.ERROR, 'number_format': '0%'}))

    def present_resource_utilization_plan_header(self, page: ExcelPage):
        page.write_cell(row=0, col=0, cell=ExcelCell(value='id ресурса'))
        page.write_cell(row=0, col=1, cell=ExcelCell(value='Название'))
        page.write_cell(row=0, col=2, cell=ExcelCell(value='Бизнес-линия'))
        page.write_cell(row=0, col=3, cell=ExcelCell(value='id задачи'))
        page.write_cell(row=0, col=4, cell=ExcelCell(value='Название задачи'))

        self.present_resource_utilization_plan_dates_header(start_row=0, start_column=5, page=page)

    def present_resource_utilization_hours(self, row: int, start_column: int, task: ResourceUtilizationTaskOutput, page: ExcelPage):
        task_hours_spent_by_day = task.hours_spent_by_day
        for i, date in enumerate(generate_date_range(self.plan_output.start_date, self.plan_output.end_date)):
            if date in task_hours_spent_by_day:
                hours_spent = task_hours_spent_by_day[date]
                page.write_cell(row=row, col=start_column + i, cell=ExcelCell(value=hours_spent,
                                                                              format={'number_format': '# ##0.0'}))

    def present_resource_utilization_tasks_and_return_row(self, row: int, tasks: [ResourceUtilizationTaskOutput], page: ExcelPage):

        for task in tasks:
            page.write_cell(row=row, col=3, cell=ExcelCell(value=task.id))
            page.write_cell(row=row, col=4, cell=ExcelCell(value=task.name))
            self.present_resource_utilization_hours(row=row, start_column=5, task=task, page=page)
            page.collapse_row(row=row, level=1)
            row = row + 1

        return row

    def present_resource_utilization_plan_data(self, resources: ResourceCalendarPlanMemberOutput, page: ExcelPage):
        row = 1
        for resource in resources:
            page.write_cell(row=row, col=0, cell=ExcelCell(value=resource.id))
            page.write_cell(row=row, col=1, cell=ExcelCell(value=resource.name))
            page.write_cell(row=row, col=2, cell=ExcelCell(value=resource.business_line))
            self.present_resources_utilization_percent(row=row, start_column=5, resource=resource, page=page)
            row = row + 1
            row = self.present_resource_utilization_tasks_and_return_row(row=row, tasks=resource.tasks, page=page)


    def present(self):
        page = self.report.add_page_named('out_Утилизация ресурсов')
        self.present_resource_utilization_plan_header(page=page)
        self.present_resource_utilization_plan_data(resources=self.plan_output.resource_utilization.resources, page=page)
        page.freeze_row_and_column(top_row=1, left_column=5)
        page.auto_fit_column(0)
        page.set_column_width(col=1, width=16)
        page.auto_fit_column(2)
        page.auto_fit_column(3)
        page.set_column_width(col=4, width=64)
        page.auto_fit_column(5)