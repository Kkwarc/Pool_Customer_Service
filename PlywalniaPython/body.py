import datetime
from datetime import date


class Body:
    """
    Includes a set of time related methods.
    """
    def get_day_of_the_week(self, booking_date):
        """
        Returns the day of the week from a given date.
        """
        year, month, day = (int(x) for x in booking_date.split('-'))
        booking_date = datetime.date(year, month, day)
        day_of_the_week = booking_date.strftime('%a')
        return day_of_the_week

    def checking_structure_date(self, booking_date):
        """
        Checks if the date structure is correct.
        """
        try:
            year, month, day = (int(x) for x in booking_date.split('-'))
            return year, month, day
        except ValueError:
            return False
        except SyntaxError:
            return False

    def checking_date(self, year, month, day):
        """
        Validates a range of days and months.
        """
        if day not in range(1, 32) or month not in range(1, 13):
            return False
        return True

    def checking_year_compared_to_now(self, booking_date):
        """
        Checks if a given date is later than the current date.
        """
        date_now = date.today()
        year, month, day = (int(x) for x in booking_date.split('-'))
        booking_date = datetime.date(year, month, day)
        if booking_date > date_now:
            return True
        return False

    def checking_time(self, booking_date):
        """
        Collects all date check functions and returns date if it is valid.
        """
        if not self.checking_structure_date(booking_date):
            return False
        year, month, day = self.checking_structure_date(booking_date)
        if not self.checking_date(year, month, day):
            return False
        booking_date = str(datetime.date(year, month, day))
        return booking_date

    def checking_hour(self, sp, hour):
        """
        Checks if the given time is within the working hours of the swimming pool.
        """
        if hour not in range(sp.get_work_hours()[0], sp.get_work_hours()[1] + 1):
            return False
        return int(hour)

    def time_of_day(self, hour):
        """
        Returns the time of day based on an hour.
        """
        if int(hour) in range(0, 12):
            time_of_day = 'before_noon'
        elif int(hour) in range(12, 24):
            time_of_day = 'after_noon'
        return time_of_day
