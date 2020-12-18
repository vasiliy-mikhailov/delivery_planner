from datetime import date
from Entities.Resource.Calendar.Calendar import Calendar


class SatSunHolidaysCalendar(Calendar):
    def is_working_day(self, day: date):
        return day.weekday() < 5

