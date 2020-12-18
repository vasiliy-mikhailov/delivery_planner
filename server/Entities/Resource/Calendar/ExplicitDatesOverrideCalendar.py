from datetime import date
from Entities.Resource.Calendar.Calendar import Calendar


class ExplicitDatesOverrideCalendar(Calendar):
    def __init__(self, explicit_workdays: [date], explicit_holidays: [date], child_calendar: Calendar):
        super().__init__()
        self.explicit_workdays: [date] = explicit_workdays
        self.explicit_holidays: [date] = explicit_holidays
        self.child_calendar: Calendar = child_calendar

    def is_working_day(self, day: date):
        if day in self.explicit_workdays:
            return True

        if day in self.explicit_holidays:
            return False

        return self.child_calendar.is_working_day(day)
