import os

from Repository.ExternalTaskRepository.ExcelExternalTaskRepository import ExcelExternalTaskRepository
from Repository.ExcelPlanReader import ExcelPlanReader
from Interactors.PlannerInteractor.PlannerInteractor import PlannerInteractor
from Presenters.ExcelPlanPresenter.ExcelPlanPresenter import ExcelPlanPresenter


def test_presenter_for_plan2_xlsx():
    reader = ExcelPlanReader(file_name_or_io='./SmallTests/input_excels/Plan2.xlsx')

    plan_input = reader.read()
    external_task_repository = ExcelExternalTaskRepository(file_name_or_io='./SmallTests/input_excels/external_tasks.xlsx')
    planner = PlannerInteractor(plan_input=plan_input, external_task_repository=external_task_repository)
    plan_output = planner.interact()

    report_file_name = './SmallTests/output_excels/test_presenter_for_plan2.xlsx'
    presenter = ExcelPlanPresenter(report_file_name_or_io=report_file_name, plan_output=plan_output)

    _ = presenter.present()

    assert os.path.exists(report_file_name)