import os

from Repository.ExcelPlanReader import ExcelPlanReader
from Interactors.PlannerInteractor.PlannerInteractor import PlannerInteractor
from Presenters.ExcelPlanPresenter.ExcelPlanPresenter import ExcelPlanPresenter
from Repository.ExternalTaskReader.ExternalTaskRowsToExternalTaskInputsDataConverter import \
    ExternalTaskRowsToExternalTaskInputsDataConverter
from Repository.ExternalTaskReader.FlatFileExternalTaskRowsReader import FlatFileExternalTaskRowsReader


def test_presenter_for_plan2_xlsx():
    reader = ExcelPlanReader(file_name='./SmallTests/input_excels/Plan2.xlsx')

    plan_input = reader.read()
    external_task_reader = FlatFileExternalTaskRowsReader(file_name='./SmallTests/input_excels/external_tasks.xlsx')
    external_task_inputs_data_converter = ExternalTaskRowsToExternalTaskInputsDataConverter(
        external_task_rows_reader=external_task_reader)
    external_task_inputs = external_task_inputs_data_converter.convert()
    planner = PlannerInteractor(plan_input=plan_input, external_task_inputs=external_task_inputs)
    plan_output = planner.interact()

    report_file_name = './SmallTests/output_excels/test_presenter_for_plan2.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    _ = presenter.present()

    assert os.path.exists(report_file_name)