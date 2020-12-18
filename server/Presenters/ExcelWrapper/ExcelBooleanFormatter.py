class ExcelBooleanFormatter:

    def format(self, value: bool) -> str:
        if value:
            return 'Да'
        else:
            return 'Нет'