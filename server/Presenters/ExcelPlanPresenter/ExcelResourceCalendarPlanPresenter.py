from Entities.Resource.Calendar.Calendar import generate_date_range
from Outputs.HightlightOutput import HighlightOutput
from Outputs.PlanOutput import PlanOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanBottleneckHintOutput import \
    ResourceCalendarPlanBottleneckHintOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanGroupOutput import ResourceCalendarPlanGroupOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanMemberOutput import ResourceCalendarPlanMemberOutput
from Outputs.ResourceCalendarPlanOutputs.ResourceCalendarPlanTaskOutput import ResourceCalendarPlanTaskOutput
from Presenters.ExcelWrapper.ExcelAbilityFormatter import ExcelAbilityFormatter
from Presenters.ExcelWrapper.ExcelBooleanFormatter import ExcelBooleanFormatter
from Presenters.ExcelWrapper.ExcelCell import ExcelCell
from Presenters.ExcelWrapper.ExcelPage import ExcelPage
from Presenters.ExcelWrapper.ExcelReport import ExcelReport


class ExcelResourceCalendarPlanPresenter:

    def __init__(self, plan_output: PlanOutput, report: ExcelReport):
        self.plan_output: PlanOutput = plan_output
        self.report: ExcelReport = report


    def present_resource_calendar_dates_header(self, start_row: int, start_column: int, page: ExcelPage):
        for i, date in enumerate(generate_date_range(self.plan_output.start_date, self.plan_output.end_date)):
            page.write_cell(row=start_row, col=start_column + i, cell=ExcelCell(value=date, format={'number_format': 'DD.MM'}))

    def present_resource_calendar_plan_header(self, page: ExcelPage):
        page.write_cell(row=0, col=0, cell=ExcelCell(value='id'))
        page.write_cell(row=0, col=1, cell=ExcelCell(value='Бизнес-линия'))
        page.write_cell(row=0, col=2, cell=ExcelCell(value='Задача'))
        page.write_cell(row=0, col=3, cell=ExcelCell(value='Подзадача'))
        page.write_cell(row=0, col=4, cell=ExcelCell(value='Подподзадача'))
        page.write_cell(row=0, col=5, cell=ExcelCell(value='Предшественники'))
        page.write_cell(row=0, col=6, cell=ExcelCell(value='Система'))
        page.write_cell(row=0, col=7, cell=ExcelCell(value='Работа'))
        page.write_cell(row=0, col=8, cell=ExcelCell(value='Ресурс'))
        page.write_cell(row=0, col=9, cell=ExcelCell(value='Ботлнек?'))
        page.write_cell(row=0, col=10, cell=ExcelCell(value='Дата начала'))
        page.write_cell(row=0, col=11, cell=ExcelCell(value='Дата окончания'))
        page.write_cell(row=0, col=12, cell=ExcelCell(value='Требуется (часы)'))
        page.write_cell(row=0, col=13, cell=ExcelCell(value='Запланировано (часы)'))
        page.write_cell(row=0, col=14, cell=ExcelCell(value='Планируемая готовность'))

        self.present_resource_calendar_dates_header(start_row=0, start_column=15, page=page)

    def present_resources_effort_decrease(self, row: int, start_column: int, resource: ResourceCalendarPlanMemberOutput, page: ExcelPage):
        for date, effort_decrease_hours in resource.effort_decreases_by_date.items():
            days_passed = (date - self.plan_output.start_date).days
            page.write_cell(row=row, col=start_column + days_passed, cell=ExcelCell(value=effort_decrease_hours, format={'number_format': '# ##0.0'}))

    def present_groups_and_return_row(self, start_row: int, groups: [ResourceCalendarPlanGroupOutput], page: ExcelPage):
        row = start_row

        excel_ability_formatter = ExcelAbilityFormatter()

        for group in groups:
            system = group.system
            ability = group.ability
            ability_str = excel_ability_formatter.format(ability)
            initial_hours = group.initial_hours
            planned_hours = group.planned_hours
            planned_readiness = group.planned_readiness
            highlight = group.highlight
            is_bottleneck = group.is_bottleneck
            boolean_formatter = ExcelBooleanFormatter()
            is_bottleneck_str = boolean_formatter.format(is_bottleneck)
            page.write_cell(row=row, col=6, cell=ExcelCell(value=system))
            page.write_cell(row=row, col=7, cell=ExcelCell(value=ability_str))
            page.write_cell(row=row, col=9, cell=ExcelCell(value=is_bottleneck_str, format={'highlight': highlight}))
            page.write_cell(row=row, col=12, cell=ExcelCell(value=initial_hours, format={'number_format': '# ##0.0'}))
            page.write_cell(row=row, col=13, cell=ExcelCell(value=planned_hours, format={'number_format': '# ##0.0'}))
            page.write_cell(row=row, col=14, cell=ExcelCell(value=planned_readiness, format={'number_format': '0%', 'highlight': highlight}))
            page.collapse_row(row=row, level=3)
            members = group.members
            row = row + 1
            row = self.present_members_and_return_row(start_row=row, members=members, page=page)

        return row

    def present_members_and_return_row(self, start_row: int, members: [ResourceCalendarPlanMemberOutput], page: ExcelPage):
        row = start_row

        for member in members:
            page.write_cell(row=row, col=8, cell=ExcelCell(value=member.resource_name, format={'highlight': member.highlight}))
            page.write_cell(row=row, col=10, cell=ExcelCell(value=member.start_date_or_empty_string, format={'highlight': member.start_date_highlight, 'number_format': 'DD.MM.YYYY'}))
            page.write_cell(row=row, col=11, cell=ExcelCell(value=member.end_date_or_empty_string, format={'highlight': member.end_date_highlight, 'number_format': 'DD.MM.YYYY'}))
            page.write_cell(row=row, col=13, cell=ExcelCell(value=member.effort_decrease_hours, format={'number_format': '# ##0.0'}))
            self.present_resources_effort_decrease(row=row, start_column=15, resource=member, page=page)
            page.collapse_row(row=row, level=3)
            row = row + 1

        return row

    def present_task_start_date_to_end_date_highlight(
            self,
            start_row: int,
            start_col: int,
            start_date_or_empty_string,
            end_date_or_empty_string,
            page: ExcelPage
    ):
        if not start_date_or_empty_string:
            return

        start_date = start_date_or_empty_string

        end_date = end_date_or_empty_string or self.plan_output.end_date

        for date in generate_date_range(start_date, end_date):
            days_from_start = (date - self.plan_output.start_date).days
            page.write_cell(
                row=start_row,
                col=start_col + days_from_start,
                cell=ExcelCell(
                    value='',
                    format={'highlight': HighlightOutput.GANTT_FILLER}
                )
            )

    def present_bottleneck_hints(self, row: int, col: int, bottleneck_hints: [ResourceCalendarPlanBottleneckHintOutput], page: ExcelPage):
        if bottleneck_hints:
            ability_formatter = ExcelAbilityFormatter()
            bottleneck_hints_strs: [str] = ["{} {} {}".format(
                hint.task_id,
                ability_formatter.format(ability=hint.ability),
                hint.system
            ) for hint in bottleneck_hints]
            bottleneck_hints_str: str = "\n".join(bottleneck_hints_strs)
            page.set_hint_for_row_and_col(row=row, col=11, hint=bottleneck_hints_str)


    def present_calendar_plan_tasks_and_return_row(self, level: int, start_row: int, tasks: [ResourceCalendarPlanTaskOutput], page: ExcelPage) -> int:
        row = start_row
        for task in tasks:
            page.write_cell(row=row, col=0, cell=ExcelCell(value=task.id))
            page.write_cell(row=row, col=1, cell=ExcelCell(value=task.business_line))
            page.write_cell(row=row, col=2 + level - 1, cell=ExcelCell(value=task.name))
            predecessor_ids = ';'.join(task.predecessor_ids)
            page.write_cell(row=row, col=5, cell=ExcelCell(value=predecessor_ids))
            page.write_cell(row=row, col=10, cell=ExcelCell(value=task.start_date_or_empty_string, format={'highlight': task.start_date_highlight, 'number_format': 'DD.MM.YYYY'}))
            page.write_cell(row=row, col=11, cell=ExcelCell(value=task.end_date_or_empty_string, format={'highlight': task.end_date_highlight, 'number_format': 'DD.MM.YYYY'}))

            self.present_bottleneck_hints(row=row, col=11, bottleneck_hints=task.bottleneck_hints, page=page)

            page.write_cell(row=row, col=12,
                            cell=ExcelCell(value=task.initial_effort_hours, format={'number_format': '# ##0.0'}))
            page.write_cell(row=row, col=13,
                            cell=ExcelCell(value=task.assigned_effort_hours, format={'number_format': '# ##0.0'}))
            page.write_cell(row=row, col=14, cell=ExcelCell(value=task.planned_readiness,
                                                           format={'highlight': task.planned_readiness_highlight,
                                                                   'number_format': '0%'}))

            self.present_task_start_date_to_end_date_highlight(
                start_row=row,
                start_col=15,
                start_date_or_empty_string=task.start_date_or_empty_string,
                end_date_or_empty_string=task.end_date_or_empty_string,
                page=page
            )

            if level >= 2:
                page.collapse_row(row=row, level=level - 1)

            row = row + 1

            row = self.present_groups_and_return_row(start_row=row, groups=task.groups, page=page)

            sub_tasks = task.sub_tasks
            row = self.present_calendar_plan_tasks_and_return_row(level=level + 1, start_row=row, tasks=sub_tasks, page=page)

        return row

    def present_resource_calendar_plan_data(self, tasks: [ResourceCalendarPlanTaskOutput], page: ExcelPage):
        self.present_calendar_plan_tasks_and_return_row(level=1, start_row=1, tasks=tasks, page=page)


    def present(self):
        page = self.report.add_page_named('out_Ресурсно-календарный план')

        self.present_resource_calendar_plan_header(page=page)
        self.present_resource_calendar_plan_data(tasks=self.plan_output.resource_calendar_plan.tasks, page=page)
        page.freeze_row_and_column(top_row=1, left_column=12)
        page.auto_fit_column(0)
        page.auto_fit_column(1)
        page.set_column_width(2, 4)
        page.set_column_width(3, 4)
        page.set_column_width(4, 60)
        page.set_column_width(5, 15)
        page.set_column_width(6, 10)
        page.set_column_width(7, 10)
        page.set_column_width(8, 10)
        page.set_column_width(9, 10)
        page.set_column_width(10, 10)
        page.auto_fit_column(11)
        page.auto_fit_column(12)
        page.auto_fit_column(13)
        page.auto_fit_column(14)