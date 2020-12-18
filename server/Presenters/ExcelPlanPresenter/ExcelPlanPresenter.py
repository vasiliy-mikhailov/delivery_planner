from Outputs.PlanOutput import PlanOutput
from Presenters.ExcelPlanPresenter.ExcelExternalTasksPagePresenter import ExcelExternalTasksPagePresenter
from Presenters.ExcelPlanPresenter.ExcelInputTaskTreePresenter import ExcelInputTaskTreePresenter
from Presenters.ExcelPlanPresenter.ExcelPlanPeriodPresenter import ExcelPlanPeriodPresenter
from Presenters.ExcelPlanPresenter.ExcelTaskResourceSupplyPresenter import \
    ExcelTaskResourceSupplyPresenter
from Presenters.ExcelPlanPresenter.ExcelResourceCalendarPlanPresenter import ExcelResourceCalendarPlanPresenter
from Presenters.ExcelPlanPresenter.ExcelResourceUtilizationPlanPresenter import ExcelResourceUtilizationPlanPresenter
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelPlanPresenter:

    def __init__(self, report_file_name: str, plan_output: PlanOutput):
        self.report_file_name: str = report_file_name
        self.plan_output: PlanOutput = plan_output

    def present(self):
        report = ExcelReport(excel_file_name=self.report_file_name)

        start_date = self.plan_output.start_date
        end_date = self.plan_output.end_date
        plan_period_presenter = ExcelPlanPeriodPresenter(
            start_date=start_date,
            end_date=end_date,
            report=report
        )
        plan_period_presenter.present()

        tasks = self.plan_output.tasks
        task_tree_presenter = ExcelInputTaskTreePresenter(
            tasks=tasks,
            report=report
        )
        task_tree_presenter.present()

        resource_calendar_plan_presenter = ExcelResourceCalendarPlanPresenter(
            plan_output=self.plan_output,
            report=report
        )
        resource_calendar_plan_presenter.present()

        resource_utilization_plan_presenter = ExcelResourceUtilizationPlanPresenter(
            plan_output=self.plan_output,
            report=report
        )
        resource_utilization_plan_presenter.present()

        task_resource_supply_presenter = ExcelTaskResourceSupplyPresenter(
            plan_output=self.plan_output,
            report=report
        )
        task_resource_supply_presenter.present()

        external_tasks = self.plan_output.external_tasks
        excel_external_task_presenter = ExcelExternalTasksPagePresenter(
            external_tasks=external_tasks,
            report=report
        )
        excel_external_task_presenter.present()

        report.write_to_disk_and_close()

        return report
