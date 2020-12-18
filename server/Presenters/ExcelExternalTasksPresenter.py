from Outputs.ExternalTaskOutput import ExternalTaskOutput
from Presenters.ExcelPlanPresenter.ExcelExternalTasksPagePresenter import ExcelExternalTasksPagePresenter
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelExternalTasksPresenter:

    def __init__(self, file_name: str, external_task_outputs: [ExternalTaskOutput]):
        self.file_name: str = file_name
        self.external_task_outputs: [ExternalTaskOutput] = external_task_outputs

    def present(self):
        report = ExcelReport(excel_file_name=self.file_name)

        excel_external_tasks_page_presenter = ExcelExternalTasksPagePresenter(
            external_tasks=self.external_task_outputs,
            report=report
        )
        excel_external_tasks_page_presenter.present()

        report.write_to_disk_and_close()

        return report