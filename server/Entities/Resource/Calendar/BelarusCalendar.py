from datetime import date
from Entities.Resource.Calendar.Calendar import Calendar
from Entities.Resource.Calendar.ExplicitDatesOverrideCalendar import ExplicitDatesOverrideCalendar
from Entities.Resource.Calendar.SatSunHolidaysCalendar import SatSunHolidaysCalendar


class BelarusCalendar(Calendar):
    EXPLICIT_WORKDAYS = []
    EXPLICIT_HOLIDAYS = [
        date(2021, 1, 1),
        date(2021, 1, 7),
        date(2021, 3, 8)
    ]

    def __init__(self):
        super().__init__()
        base_calendar = SatSunHolidaysCalendar()

        self.explicit_dates_override_calendar = ExplicitDatesOverrideCalendar(
            explicit_workdays=self.EXPLICIT_WORKDAYS,
            explicit_holidays=self.EXPLICIT_HOLIDAYS,
            child_calendar=base_calendar
        )

    def is_working_day(self, day: date):
        return self.explicit_dates_override_calendar.is_working_day(day)
