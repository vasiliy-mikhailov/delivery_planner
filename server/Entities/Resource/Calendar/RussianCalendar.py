from datetime import date
from Entities.Resource.Calendar.Calendar import Calendar
from Entities.Resource.Calendar.ExplicitDatesOverrideCalendar import ExplicitDatesOverrideCalendar
from Entities.Resource.Calendar.SatSunHolidaysCalendar import SatSunHolidaysCalendar


class RussianCalendar(Calendar):
    EXPLICIT_WORKDAYS = [date(2021, 2, 20)]
    EXPLICIT_HOLIDAYS = [
        date(2020, 11, 4),
        date(2021, 1, 1),
        date(2021, 1, 4),
        date(2021, 1, 5),
        date(2021, 1, 6),
        date(2021, 1, 7),
        date(2021, 1, 8),
        date(2021, 2, 22),
        date(2021, 2, 23),
        date(2021, 3, 8),
        date(2021, 5, 3),
        date(2021, 5, 10),
        date(2021, 6, 14),
        date(2021, 11, 4),
        date(2021, 11, 5),
        date(2021, 12, 31)
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
