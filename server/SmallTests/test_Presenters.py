import os
import datetime
from Repository.ExcelPlanReader import ExcelPlanReader
from Interactors.PlannerInteractor.PlannerInteractor import PlannerInteractor
from Outputs.HightlightOutput import HighlightOutput
from Outputs.PlanOutput import PlanOutput
from Presenters.ExcelPlanPresenter.ExcelPlanPresenter import ExcelPlanPresenter
from Presenters.ExcelWrapper.ExcelBooleanFormatter import ExcelBooleanFormatter
from Presenters.ExcelWrapper.ExcelReport import ExcelReport
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
import pytest
from Presenters.ExcelWrapper.ExcelAbilityFormatter import ExcelAbilityFormatter
from Repository.ExternalTaskReader.ExcelExternalTaskInputsReader import ExcelExternalTaskRowsReader
from Repository.ExternalTaskReader.ExternalTaskRowsToExternalTaskInputsDataConverter import \
    ExternalTaskRowsToExternalTaskInputsDataConverter
from SmallTests.FakeExternalTaskRowsReader import FakeExternalTaskRowsReader
from SmallTests.FakePlanReader import FakePlanReader
from SmallTests.FakePlannerInteractor import FakePlanner
from Entities.Skill.AbilityEnum import AbilityEnum


def test_excel_report_creates_file():
    excel_file_name = './SmallTests/output_excels/test_excel_report_creates_file.xlsx'
    if os.path.exists(excel_file_name):
        os.remove(excel_file_name)

    report = ExcelReport(excel_file_name)

    report.write_to_disk_and_close()

    assert os.path.exists(excel_file_name)
    os.remove(excel_file_name)


def test_excel_report_creates_page():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_excel_report_creates_page.xlsx')
    page = report.add_page_named(page_name='Bar')
    assert isinstance(page, ExcelPage)
    assert page.get_name() == 'Bar'

    assert 'Bar' in report.get_page_names()
    page = report.get_page_by_name('Bar')
    assert isinstance(page, ExcelPage)
    assert page.get_name() == 'Bar'

    report.write_to_disk_and_close()


def test_excel_report_throws_error_if_does_not_find_page():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_excel_report_throws_error_if_does_not_find_page.xlsx')
    report.add_page_named(page_name='Bar')
    report.write_to_disk_and_close()

    with pytest.raises(ValueError):
        report.get_page_by_name('Buz')


def test_excel_page_holds_data():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_excel_page_holds_data.xlsx')
    page = report.add_page_named(page_name='Bar')
    report.write_to_disk_and_close()

    assert page.get_name() == 'Bar'


def test_excel_page_freezes_row_and_column_and_returns_frozen_row_and_column():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_excel_page_freezes_row_and_column_and_returns_frozen_row_and_column.xlsx')
    page = report.add_page_named(page_name='Bar')
    page.freeze_row_and_column(top_row=1, left_column=2)
    report.write_to_disk_and_close()

    assert page.get_frozen_row_and_column() == (1, 2)

def test_get_frozen_row_and_column_raises_value_error_if_was_not_frozen():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_get_frozen_row_and_column_raises_value_error_if_was_not_frozen.xlsx')
    page = report.add_page_named(page_name='Bar')
    report.write_to_disk_and_close()

    with pytest.raises(ValueError):
        _ = page.get_frozen_row_and_column() == (1, 2)


def test_get_hint_for_row_and_column_returns_previously_supplied_data():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_get_hint_for_row_and_column_returns_previously_supplied_data.xlsx')
    page = report.add_page_named(page_name='Bar')
    page.set_hint_for_row_and_col(row=0, col=1, hint='Foo')
    report.write_to_disk_and_close()
    assert page.get_hint_for_row_and_col(row=0, col=1) == 'Foo'

def test_excel_cell_holds_data():
    excel_cell = ExcelCell(value='Foo', format={'highlight': HighlightOutput.REGULAR, 'number_format': '0%'})
    assert excel_cell.value == 'Foo'
    assert excel_cell.highlight == HighlightOutput.REGULAR
    assert excel_cell.number_format == '0%'

def test_excel_cell_raises_value_error_when_supplied_with_nan():
    with pytest.raises(ValueError):
        _ = ExcelCell(value=float('nan'), format={'highlight': HighlightOutput.REGULAR, 'number_format': '0%'})


def test_excel_cell_highlights_data():
    regular_cell = ExcelCell(value='Foo')
    assert len(regular_cell.get_excel_format_properties().keys()) == 0

    warning_cell = ExcelCell(value='Foo', format={'highlight': HighlightOutput.WARNING})
    assert warning_cell.get_excel_format_properties()['font_color'] == 'black'
    assert warning_cell.get_excel_format_properties()['bg_color'] == 'yellow'

    error_cell = ExcelCell(value='Foo', format={'highlight': HighlightOutput.ERROR})
    assert error_cell.get_excel_format_properties()['font_color'] == 'white'
    assert error_cell.get_excel_format_properties()['bg_color'] == 'red'

    gantt_cell = ExcelCell(value='Foo', format={'highlight': HighlightOutput.GANTT_FILLER})
    assert gantt_cell.get_excel_format_properties()['font_color'] == 'white'
    assert gantt_cell.get_excel_format_properties()['bg_color'] == 'gray'


def test_excel_page_writes_data():
    report = ExcelReport('./SmallTests/output_excels/test_excel_page_writes_data.xlsx')
    page = report.add_page_named('Bar')
    cell = ExcelCell(value='Buz', format={'highlight': HighlightOutput.REGULAR})
    page.write_cell(row=0, col=0, cell=cell)
    assert page.read_cell(row=0, col=0).value == 'Buz'
    assert page.read_cell(row=0, col=0).highlight == HighlightOutput.REGULAR
    report.write_to_disk_and_close()


def test_yes_no_excel_formatter_outputs_da_and_net():
    formatter = ExcelBooleanFormatter()

    assert formatter.format(True) == 'Да'
    assert formatter.format(False) == 'Нет'

def test_ability_formatter_outputs_ability_name():
    formatter = ExcelAbilityFormatter()

    assert formatter.format(AbilityEnum.SOLUTION_ARCHITECTURE) == 'Архитектура решения'
    assert formatter.format(AbilityEnum.SYSTEM_ANALYSIS) == 'Системный анализ'
    assert formatter.format(AbilityEnum.DEVELOPMENT) == 'Разработка'
    assert formatter.format(AbilityEnum.SYSTEM_TESTING) == 'Системное тестирование'
    assert formatter.format(AbilityEnum.INTEGRATION_TESTING) == 'Интеграционное тестирование'
    assert formatter.format(AbilityEnum.PRODUCT_OWNERSHIP) == 'Управление продуктом'
    assert formatter.format(AbilityEnum.PROJECT_MANAGEMENT) == 'Управление проектом'

def test_plan_presenter_shows_plan_period():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    report_file_name = './SmallTests/output_excels/test_plan_presenter_shows_task_resource_supply.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    report = presenter.present()

    assert os.path.exists(report_file_name)
    plan_period_page = report.get_page_by_name('Период расчета')
    assert plan_period_page.read_cell(row=0, col=0).value == 'Начало'
    assert plan_period_page.read_cell(row=0, col=1).value == datetime.date(2020, 10, 5)
    assert plan_period_page.read_cell(row=0, col=1).number_format == 'dd.mm.yyyy'
    assert plan_period_page.read_cell(row=1, col=0).value == 'Окончание'
    assert plan_period_page.read_cell(row=1, col=1).value == datetime.date(2021, 2, 5)
    assert plan_period_page.read_cell(row=1, col=1).number_format == 'dd.mm.yyyy'

def test_plan_presenter_shows_tasks():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    report_file_name = './SmallTests/output_excels/test_plan_presenter_shows_tasks.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    report = presenter.present()

    assert os.path.exists(report_file_name)
    tasks_page = report.get_page_by_name('Заявки')
    assert tasks_page.read_cell(row=0, col=0).value == 'id'
    assert tasks_page.read_cell(row=0, col=1).value == 'Бизнес-линия'
    assert tasks_page.read_cell(row=0, col=2).value == 'Заявка на доработку ПО'
    assert tasks_page.read_cell(row=0, col=3).value == 'Заявка на доработку системы'
    assert tasks_page.read_cell(row=0, col=4).value == 'Подзадача'
    assert tasks_page.read_cell(row=0, col=5).value == 'Предшественники'
    assert tasks_page.read_cell(row=0, col=6).value == 'Система'
    assert tasks_page.read_cell(row=0, col=7).value == 'Работа'
    assert tasks_page.read_cell(row=0, col=8).value == 'Количество или id ресурса'
    assert tasks_page.read_cell(row=0, col=9).value == 'Архитектор решения (осталось часов)'
    assert tasks_page.read_cell(row=0, col=10).value == 'Системный аналитик (осталось часов)'
    assert tasks_page.read_cell(row=0, col=11).value == 'Разработчик (осталось часов)'
    assert tasks_page.read_cell(row=0, col=12).value == 'Системный тестировщик (осталось часов)'
    assert tasks_page.read_cell(row=0, col=13).value == 'Интеграционный тестировщик (осталось часов)'
    assert tasks_page.read_cell(row=0, col=14).value == 'Владелец продукта (осталось часов)'
    assert tasks_page.read_cell(row=0, col=15).value == 'Руководитель проекта (осталось часов)'

    assert tasks_page.read_cell(row=1, col=0).value == 'CR-1'
    assert tasks_page.read_cell(row=1, col=1).value == 'BL-1'
    assert tasks_page.read_cell(row=1, col=2).value == 'Change Request 1'
    assert tasks_page.read_cell(row=1, col=9).value == 80
    assert tasks_page.read_cell(row=1, col=9).number_format == '# ##0.0'
    assert tasks_page.read_cell(row=1, col=13).value == 40
    assert tasks_page.read_cell(row=1, col=13).number_format == '# ##0.0'
    assert tasks_page.read_cell(row=1, col=14).value == 80
    assert tasks_page.read_cell(row=1, col=14).number_format == '# ##0.0'

    assert tasks_page.read_cell(row=4, col=0).value == 'DEV-1.1.1'
    assert tasks_page.read_cell(row=4, col=1).value == 'BL-1'
    assert tasks_page.read_cell(row=4, col=4).value == 'Development 1.1'
    assert tasks_page.read_cell(row=4, col=5).value == 'SYSAN-1.1.1'
    assert tasks_page.read_cell(row=4, col=6).value == 'SYS-1'
    assert tasks_page.read_cell(row=4, col=11).value == 120
    assert tasks_page.read_cell(row=4, col=11).number_format == '# ##0.0'

    assert tasks_page.read_cell(row=7, col=7).value == 'Системная аналитика'
    assert tasks_page.read_cell(row=7, col=8).value == 'solar@my.com'

    assert tasks_page.read_cell(row=8, col=7).value == 'Разработка'
    assert tasks_page.read_cell(row=8, col=8).value == 1

def test_plan_presenter_shows_task_resource_supply():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    report_file_name = './SmallTests/output_excels/test_plan_presenter_shows_task_resource_supply.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    report = presenter.present()

    assert os.path.exists(report_file_name)
    task_resource_supply_page = report.get_page_by_name('out_Обеспеченность ресурсами')
    assert task_resource_supply_page.read_cell(row=0, col=0).value == 'id заявки'
    assert task_resource_supply_page.read_cell(row=0, col=0).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=2, col=0).value == 'CR-1'
    assert task_resource_supply_page.read_cell(row=2, col=0).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=3, col=0).value == 'CR-2'
    assert task_resource_supply_page.read_cell(row=3, col=0).highlight == HighlightOutput.REGULAR

    assert task_resource_supply_page.read_cell(row=0, col=1).value == 'Название'
    assert task_resource_supply_page.read_cell(row=0, col=1).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=2, col=1).value == 'Change Request 1'
    assert task_resource_supply_page.read_cell(row=2, col=1).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=3, col=1).value == 'Change Request 2'
    assert task_resource_supply_page.read_cell(row=3, col=1).highlight == HighlightOutput.REGULAR

    assert task_resource_supply_page.read_cell(row=0, col=2).value == 'Бизнес-линия'
    assert task_resource_supply_page.read_cell(row=0, col=2).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=2, col=2).value == 'BL-1'
    assert task_resource_supply_page.read_cell(row=2, col=2).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=3, col=2).value == 'BL-2'
    assert task_resource_supply_page.read_cell(row=3, col=2).highlight == HighlightOutput.REGULAR

    assert task_resource_supply_page.read_cell(row=0, col=3).value == 'Хватает ресурсов?'
    assert task_resource_supply_page.read_cell(row=0, col=3).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=2, col=3).value == 'Да'
    assert task_resource_supply_page.read_cell(row=2, col=3).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=3, col=3).value == 'Нет'
    assert task_resource_supply_page.read_cell(row=3, col=3).highlight == HighlightOutput.ERROR

    excel_ability_formatter = ExcelAbilityFormatter()
    assert task_resource_supply_page.read_cell(row=0, col=4).value == excel_ability_formatter.format(AbilityEnum.SOLUTION_ARCHITECTURE)
    assert task_resource_supply_page.read_cell(row=0, col=4).highlight == HighlightOutput.REGULAR

    assert task_resource_supply_page.read_cell(row=2, col=4).value == 1.0
    assert task_resource_supply_page.read_cell(row=2, col=4).highlight == HighlightOutput.REGULAR
    assert task_resource_supply_page.read_cell(row=2, col=4).number_format == '0%'
    assert task_resource_supply_page.read_cell(row=3, col=4).value == 0.0
    assert task_resource_supply_page.read_cell(row=3, col=4).number_format == '0%'
    assert task_resource_supply_page.read_cell(row=3, col=4).highlight == HighlightOutput.ERROR

    assert task_resource_supply_page.get_frozen_row_and_column() == (2, 5)

def test_task_resource_supply_presenter_shows_excel_for_fake_data():
    fake_plan_reader = FakePlanReader()
    plan_input = fake_plan_reader.read()
    external_task_inputs_reader = FakeExternalTaskRowsReader()
    external_task_inputs_data_converter = ExternalTaskRowsToExternalTaskInputsDataConverter(
        external_task_rows_reader=external_task_inputs_reader)
    external_task_inputs = external_task_inputs_data_converter.convert()
    sut = PlannerInteractor(plan_input=plan_input, external_task_inputs=external_task_inputs)
    plan_output: PlanOutput = sut.interact()

    report_file_name = './SmallTests/output_excels/test_task_resource_supply_presenter_shows_excel_for_fake_data.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    presenter.present()

def test_plan_presenter_shows_resource_calendar_plan():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    report_file_name = './SmallTests/output_excels/test_plan_presenter_shows_resource_calendar_plan.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    report = presenter.present()

    assert os.path.exists(report_file_name)
    resource_calendar_plan_page = report.get_page_by_name('out_Ресурсно-календарный план')
    assert resource_calendar_plan_page.read_cell(row=0, col=0).value == 'id'
    assert resource_calendar_plan_page.read_cell(row=0, col=1).value == 'Бизнес-линия'
    assert resource_calendar_plan_page.read_cell(row=0, col=2).value == 'Задача'
    assert resource_calendar_plan_page.read_cell(row=0, col=3).value == 'Подзадача'
    assert resource_calendar_plan_page.read_cell(row=0, col=4).value == 'Подподзадача'
    assert resource_calendar_plan_page.read_cell(row=0, col=5).value == 'Предшественники'
    assert resource_calendar_plan_page.read_cell(row=0, col=6).value == 'Система'
    assert resource_calendar_plan_page.read_cell(row=0, col=7).value == 'Работа'
    assert resource_calendar_plan_page.read_cell(row=0, col=8).value == 'Ресурс'
    assert resource_calendar_plan_page.read_cell(row=0, col=9).value == 'Ботлнек?'
    assert resource_calendar_plan_page.read_cell(row=0, col=10).value == 'Дата начала'
    assert resource_calendar_plan_page.read_cell(row=0, col=11).value == 'Дата окончания'
    assert resource_calendar_plan_page.read_cell(row=0, col=12).value == 'Требуется (часы)'
    assert resource_calendar_plan_page.read_cell(row=0, col=13).value == 'Запланировано (часы)'
    assert resource_calendar_plan_page.read_cell(row=0, col=14).value == 'Планируемая готовность'
    assert resource_calendar_plan_page.read_cell(row=0, col=15).value == datetime.date(2020, 10, 5)
    assert resource_calendar_plan_page.read_cell(row=0, col=16).number_format == 'DD.MM'
    assert resource_calendar_plan_page.read_cell(row=0, col=138).value == datetime.date(2021, 2, 5)
    assert resource_calendar_plan_page.read_cell(row=0, col=138).number_format == 'DD.MM'

    assert resource_calendar_plan_page.read_cell(row=1, col=0).value == 'CR-1'
    assert resource_calendar_plan_page.read_cell(row=1, col=1).value == 'BL-1'
    assert resource_calendar_plan_page.read_cell(row=1, col=2).value == 'Заявка на доработку ПО'
    assert resource_calendar_plan_page.read_cell(row=1, col=10).value == datetime.date(2020, 10, 5)
    assert resource_calendar_plan_page.read_cell(row=1, col=10).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=1, col=10).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=1, col=11).value == datetime.date(2021, 4, 16)
    assert resource_calendar_plan_page.read_cell(row=1, col=11).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=1, col=11).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.get_hint_for_row_and_col(row=1, col=11) == 'CR-1 Разработка SYS-1'
    assert resource_calendar_plan_page.read_cell(row=1, col=12).value == 2520
    assert resource_calendar_plan_page.read_cell(row=1, col=12).number_format == '# ##0.0'
    assert resource_calendar_plan_page.read_cell(row=1, col=13).value == 2520
    assert resource_calendar_plan_page.read_cell(row=1, col=14).value == 1
    assert resource_calendar_plan_page.read_cell(row=1, col=14).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=1, col=14).number_format == '0%'
    assert resource_calendar_plan_page.read_cell(row=1, col=15).highlight == HighlightOutput.GANTT_FILLER

    assert resource_calendar_plan_page.read_cell(row=2, col=3).value == 'Архитектура решения'
    assert resource_calendar_plan_page.read_cell(row=2, col=10).value == datetime.date(2020, 11, 5)
    assert resource_calendar_plan_page.read_cell(row=2, col=10).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=2, col=10).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=2, col=11).value == ''
    assert resource_calendar_plan_page.read_cell(row=2, col=11).highlight == HighlightOutput.ERROR
    assert resource_calendar_plan_page.read_cell(row=2, col=11).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=2, col=12).value == 81.9
    assert resource_calendar_plan_page.read_cell(row=2, col=12).number_format == '# ##0.0'
    assert resource_calendar_plan_page.read_cell(row=2, col=14).value == 0.95
    assert resource_calendar_plan_page.read_cell(row=2, col=14).highlight == HighlightOutput.ERROR
    assert resource_calendar_plan_page.read_cell(row=2, col=14).number_format == '0%'
    assert resource_calendar_plan_page.read_cell(row=2, col=46).highlight == HighlightOutput.GANTT_FILLER
    assert resource_calendar_plan_page.get_collapse_level_for_row(row=2) == 1

    assert resource_calendar_plan_page.read_cell(row=3, col=6).value == 'SYS-1'
    assert resource_calendar_plan_page.read_cell(row=3, col=7).value == 'Архитектура решения'
    assert resource_calendar_plan_page.read_cell(row=3, col=9).value == 'Да'
    assert resource_calendar_plan_page.read_cell(row=3, col=12).value == 100
    assert resource_calendar_plan_page.read_cell(row=3, col=12).number_format == '# ##0.0'
    assert resource_calendar_plan_page.read_cell(row=3, col=13).value == 80
    assert resource_calendar_plan_page.read_cell(row=3, col=13).number_format == '# ##0.0'
    assert resource_calendar_plan_page.read_cell(row=3, col=14).value == 0.8
    assert resource_calendar_plan_page.read_cell(row=3, col=14).number_format == '0%'
    assert resource_calendar_plan_page.get_collapse_level_for_row(row=3) == 3

    assert resource_calendar_plan_page.read_cell(row=4, col=8).value == 'Архитектор Р.А.'
    assert resource_calendar_plan_page.read_cell(row=4, col=8).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=4, col=10).value == datetime.date(2020, 11, 5)
    assert resource_calendar_plan_page.read_cell(row=4, col=10).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=4, col=10).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=4, col=11).value == ''
    assert resource_calendar_plan_page.read_cell(row=4, col=11).highlight == HighlightOutput.ERROR
    assert resource_calendar_plan_page.read_cell(row=4, col=11).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=4, col=15).value == 7
    assert resource_calendar_plan_page.read_cell(row=4, col=15).number_format == '# ##0.0'
    assert resource_calendar_plan_page.read_cell(row=4, col=17).value == 5
    assert resource_calendar_plan_page.read_cell(row=4, col=17).number_format == '# ##0.0'
    assert resource_calendar_plan_page.get_collapse_level_for_row(row=4) == 3

    assert resource_calendar_plan_page.read_cell(row=5, col=3).value == 'Доработка системы'
    assert resource_calendar_plan_page.read_cell(row=5, col=5).value == 'SOLAR-1.1'
    assert resource_calendar_plan_page.read_cell(row=5, col=10).value == datetime.date(2020, 11, 5)
    assert resource_calendar_plan_page.read_cell(row=5, col=10).highlight == HighlightOutput.REGULAR
    assert resource_calendar_plan_page.read_cell(row=5, col=10).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=5, col=11).value == ''
    assert resource_calendar_plan_page.read_cell(row=5, col=11).highlight == HighlightOutput.ERROR
    assert resource_calendar_plan_page.read_cell(row=5, col=11).number_format == 'DD.MM.YYYY'
    assert resource_calendar_plan_page.read_cell(row=5, col=12).value == 220.69
    assert resource_calendar_plan_page.read_cell(row=5, col=12).number_format == '# ##0.0'
    assert resource_calendar_plan_page.read_cell(row=5, col=14).value == 0.95
    assert resource_calendar_plan_page.read_cell(row=5, col=14).highlight == HighlightOutput.ERROR
    assert resource_calendar_plan_page.read_cell(row=5, col=14).number_format == '0%'
    assert resource_calendar_plan_page.read_cell(row=5, col=46).highlight == HighlightOutput.GANTT_FILLER
    assert resource_calendar_plan_page.get_collapse_level_for_row(row=5) == 1

    assert resource_calendar_plan_page.get_frozen_row_and_column() == (1, 12)

def test_plan_presenter_shows_resource_utilization_plan():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    report_file_name = './SmallTests/output_excels/test_plan_presenter_shows_resource_utilization_plan.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    report = presenter.present()

    assert os.path.exists(report_file_name)
    resource_utilization_page = report.get_page_by_name('out_Утилизация ресурсов')
    assert resource_utilization_page.read_cell(row=0, col=0).value == 'id ресурса'
    assert resource_utilization_page.read_cell(row=0, col=1).value == 'Название'
    assert resource_utilization_page.read_cell(row=0, col=2).value == 'Бизнес-линия'
    assert resource_utilization_page.read_cell(row=0, col=3).value == 'id задачи'
    assert resource_utilization_page.read_cell(row=0, col=4).value == 'Название задачи'
    assert resource_utilization_page.read_cell(row=0, col=5).value == datetime.date(2020, 10, 5)
    assert resource_utilization_page.read_cell(row=0, col=5).number_format == 'DD.MM'

    assert resource_utilization_page.read_cell(row=1, col=0).value == 'DEV-1'
    assert resource_utilization_page.read_cell(row=1, col=1).value == 'Developer'
    assert resource_utilization_page.read_cell(row=1, col=2).value == 'BL-1'
    assert resource_utilization_page.read_cell(row=1, col=5).value == 1
    assert resource_utilization_page.read_cell(row=1, col=5).number_format == '0%'
    assert resource_utilization_page.read_cell(row=1, col=5).highlight == HighlightOutput.REGULAR

    assert resource_utilization_page.read_cell(row=2, col=3).value == 'CR-1'
    assert resource_utilization_page.read_cell(row=2, col=4).value == 'Change Request 1'
    assert resource_utilization_page.read_cell(row=2, col=5).value == 7.0
    assert resource_utilization_page.read_cell(row=2, col=5).number_format == '# ##0.0'

    assert resource_utilization_page.get_collapse_level_for_row(row=2) == 1

    assert resource_utilization_page.get_frozen_row_and_column() == (1, 5)

def test_presenter_from_real_planner_interactor_produces_output():
    fake_plan_reader = FakePlanReader()
    plan_input = fake_plan_reader.read()
    external_task_inputs_reader = FakeExternalTaskRowsReader()
    external_task_inputs_data_converter = ExternalTaskRowsToExternalTaskInputsDataConverter(
        external_task_rows_reader=external_task_inputs_reader)
    external_task_inputs = external_task_inputs_data_converter.convert()
    sut = PlannerInteractor(plan_input=plan_input, external_task_inputs=external_task_inputs)
    plan_output: PlanOutput = sut.interact()

    report_file_name = './SmallTests/output_excels/test_presenter_from_real_planner_interactor_produces_output.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    _ = presenter.present()

    assert os.path.exists(report_file_name)

def test_excel_cell_returns_column_width_for_string_date_float():
    string_cell = ExcelCell(value='Foo')
    assert string_cell.get_autofit_cell_width() == 3

    date_cell = ExcelCell(value=datetime.date(2020, 10, 5))
    assert date_cell.get_autofit_cell_width() == 10

    date_cell = ExcelCell(value=datetime.date(2020, 10, 5), format={'number_format': 'DD.MM'})
    assert date_cell.get_autofit_cell_width() == 5

    int_cell = ExcelCell(value=7, format={'number_format': '# #0.0'})
    assert int_cell.get_autofit_cell_width() == 4

    int_cell = ExcelCell(value=1000, format={'number_format': '# #0.0'})
    assert int_cell.get_autofit_cell_width() == 8

    float_cell = ExcelCell(value=7.0, format={'number_format': '# #0.0'})
    assert float_cell.get_autofit_cell_width() == 4

    float_cell = ExcelCell(value=1000.0, format={'number_format': '# #0.0'})
    assert float_cell.get_autofit_cell_width() == 8

    percent_cell = ExcelCell(value=0.01, format={'number_format': '0%'})
    assert percent_cell.get_autofit_cell_width() == 3

    percent_cell = ExcelCell(value=1, format={'number_format': '0%'})
    assert percent_cell.get_autofit_cell_width() == 5

def test_excel_page_autofits_column():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_excel_page_autofits_column.xlsx')
    page = report.add_page_named(page_name='Foo')
    page.write_cell(row=0, col=0, cell=ExcelCell('Short string'))
    page.write_cell(row=1, col=0, cell=ExcelCell('Very very very long string'))
    assert page.get_auto_fit_column_width(col=0) == 26
    page.auto_fit_column(col=0)
    page.auto_fit_all_columns()
    report.auto_fit_all_columns_on_all_pages()

def test_excel_page_collapses_row():
    report = ExcelReport(excel_file_name='./SmallTests/output_excels/test_excel_page_collapses_row.xlsx')
    page = report.add_page_named(page_name='Foo')
    page.write_cell(row=0, col=0, cell=ExcelCell('Bar'))
    page.write_cell(row=1, col=0, cell=ExcelCell('Buz'))
    page.collapse_row(row=0, level=1)
    assert page.get_collapse_level_for_row(row=0) == 1
    assert page.get_collapse_level_for_row(row=1) == 0
    report.write_to_disk_and_close()

def test_presenter_for_plan1_xlsx():
    reader = ExcelPlanReader(file_name='./SmallTests/input_excels/Plan1.xlsx')

    plan_input = reader.read()
    external_task_reader = ExcelExternalTaskRowsReader(file_name='./SmallTests/input_excels/Plan1.xlsx')
    external_task_inputs_data_converter = ExternalTaskRowsToExternalTaskInputsDataConverter(
        external_task_rows_reader=external_task_reader)
    external_task_inputs = external_task_inputs_data_converter.convert()
    planner = PlannerInteractor(plan_input=plan_input, external_task_inputs=external_task_inputs)
    plan_output = planner.interact()

    report_file_name = './SmallTests/output_excels/test_presenter_for_plan1.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    _ = presenter.present()

    assert os.path.exists(report_file_name)

def test_presenter_for_corp_transactions_xlsx():
    reader = ExcelPlanReader(file_name='./SmallTests/input_excels/Corp.Transactions.xlsx')

    plan_input = reader.read()
    external_task_reader = ExcelExternalTaskRowsReader(file_name='./SmallTests/input_excels/Corp.Transactions.xlsx')
    external_task_inputs_data_converter = ExternalTaskRowsToExternalTaskInputsDataConverter(
        external_task_rows_reader=external_task_reader)
    external_task_inputs = external_task_inputs_data_converter.convert()
    planner = PlannerInteractor(plan_input=plan_input, external_task_inputs=external_task_inputs)
    plan_output = planner.interact()

    report_file_name = './SmallTests/output_excels/Corp.Transactions.out.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    _ = presenter.present()

    assert os.path.exists(report_file_name)

def test_plan_presenter_shows_external_task():
    fake_planner = FakePlanner()
    fake_plan_reader = FakePlanReader()

    plan_input = fake_plan_reader.read()
    plan_output = fake_planner.plan(plan_input)

    report_file_name = './SmallTests/output_excels/test_plan_presenter_shows_external_task.xlsx'
    presenter = ExcelPlanPresenter(report_file_name=report_file_name, plan_output=plan_output)

    report = presenter.present()

    assert os.path.exists(report_file_name)
    external_tasks_page = report.get_page_by_name('Репозиторий задач')
    assert external_tasks_page.read_cell(row=0, col=0).value == 'id'
    assert external_tasks_page.read_cell(row=0, col=1).value == 'Бизнес-линия'
    assert external_tasks_page.read_cell(row=0, col=2).value == 'Заявка на доработку ПО'
    assert external_tasks_page.read_cell(row=0, col=3).value == 'Заявка на доработку системы'
    assert external_tasks_page.read_cell(row=0, col=4).value == 'Подзадача'
    assert external_tasks_page.read_cell(row=0, col=5).value == 'Система'
    assert external_tasks_page.read_cell(row=0, col=6).value == 'Архитектор решения (осталось часов)'
    assert external_tasks_page.read_cell(row=0, col=7).value == 'Системный аналитик (осталось часов)'
    assert external_tasks_page.read_cell(row=0, col=8).value == 'Разработчик (осталось часов)'
    assert external_tasks_page.read_cell(row=0, col=9).value == 'Системный тестировщик (осталось часов)'
    assert external_tasks_page.read_cell(row=0, col=10).value == 'Интеграционный тестировщик (осталось часов)'
    assert external_tasks_page.read_cell(row=0, col=11).value == 'Владелец продукта (осталось часов)'
    assert external_tasks_page.read_cell(row=0, col=12).value == 'Руководитель проекта (осталось часов)'

    assert external_tasks_page.read_cell(row=1, col=0).value == 'CR-1'
    assert external_tasks_page.read_cell(row=1, col=1).value == 'BL-1'
    assert external_tasks_page.read_cell(row=1, col=2).value == 'Change Request 1'
    assert external_tasks_page.read_cell(row=1, col=6).value == 80
    assert external_tasks_page.read_cell(row=1, col=6).number_format == '# ##0.0'
    assert external_tasks_page.read_cell(row=1, col=10).value == 40
    assert external_tasks_page.read_cell(row=1, col=10).number_format == '# ##0.0'
    assert external_tasks_page.read_cell(row=1, col=11).value == 80
    assert external_tasks_page.read_cell(row=1, col=11).number_format == '# ##0.0'

    assert external_tasks_page.read_cell(row=4, col=0).value == 'DEV-1.1.1'
    assert external_tasks_page.read_cell(row=4, col=1).value == 'BL-1'
    assert external_tasks_page.read_cell(row=4, col=4).value == 'Development 1.1'
    assert external_tasks_page.read_cell(row=4, col=5).value == 'SYS-1'
    assert external_tasks_page.read_cell(row=4, col=8).value == 120
    assert external_tasks_page.read_cell(row=4, col=8).number_format == '# ##0.0'

