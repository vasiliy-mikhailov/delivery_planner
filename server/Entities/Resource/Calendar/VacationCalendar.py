from datetime import date
from Entities.Resource.Calendar.Calendar import Calendar
from Entities.Resource.Calendar.ExplicitDatesOverrideCalendar import ExplicitDatesOverrideCalendar


class VacationCalendar(Calendar):

    def __init__(self, holidays: [date], working_days: [date], child_calendar: Calendar):
        super().__init__()
        self.calendar = ExplicitDatesOverrideCalendar(
            explicit_workdays = working_days,
            explicit_holidays=holidays,
            child_calendar=child_calendar
        )

    def is_working_day(self, day: date):
        return self.calendar.is_working_day(day)
