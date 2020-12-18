from xlsxwriter import Workbook
from Presenters.ExcelWrapper.ExcelPage import ExcelPage


class ExcelReport:

    def __init__(self, excel_file_name: str):
        self.excel_file_name: str = excel_file_name
        self.workbook: Workbook = Workbook(excel_file_name, {'in_memory': True})
        self.pages: [ExcelPage] = []

    def write_to_disk_and_close(self):
        self.workbook.close()

    def add_page_named(self, page_name: str):
        worksheet = self.workbook.add_worksheet(page_name)
        page = ExcelPage(worksheet=worksheet, parent_report=self)
        self.pages.append(page)
        return page

    def get_page_names(self):
        return [page.get_name() for page in self.pages]

    def get_page_by_name(self, page_name: str):
        found_pages = [page for page in self.pages if page.get_name() == page_name]

        if len(found_pages) == 1:
            return found_pages[0]
        else:
            raise ValueError('{} is not in pages'.format(page_name))

    def add_format(self, format_properties: dict):
        return self.workbook.add_format(properties=format_properties)

    def auto_fit_all_columns_on_all_pages(self):
        for page in self.pages:
            page.auto_fit_all_columns()