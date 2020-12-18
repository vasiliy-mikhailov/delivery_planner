from datetime import date, timedelta


def generate_date_range(start_date: date, end_date: date):
    current_date = start_date
    one_day = timedelta(days=1)
    while current_date <= end_date:
        yield current_date
        current_date = current_date + one_day

class Calendar:

    def __init__(self):
        pass

    def is_working_day(self, day: date):
        raise NotImplementedError
