import datetime
from swimmingpool_parameters import SCHOOLTRACKPARAMETER, PERSONPERTRACK 


class SwimmingPool:
    """
    Class: Swimming Pool
    Has: name, work_hours, price list and number of tracks
    It handles booking and payment history.
    Checks for free seats / lanes and generates a payment.
    """
    def __init__(self, name: str, work_hours: list, price_list, number_of_tracks: int):
        self._name = name
        self._work_hours = work_hours
        self._price_list = price_list
        self._number_of_tracks = number_of_tracks
        self._number_of_seats = self._number_of_tracks * PERSONPERTRACK
        self._swimming_pool_school_limit = int(SCHOOLTRACKPARAMETER * self._number_of_tracks - 0.5)
        self.booking_history = {}
        self.payment_history = {}

    def get_name(self):
        return self._name

    def get_work_hours(self):
        return [int(self._work_hours[0]), int(self._work_hours[1])]

    def get_number_of_tracks(self):
        return self._number_of_tracks

    def get_number_of_seats(self):
        return self._number_of_seats

    def get_swimming_pool_school_limit(self):
        return self._swimming_pool_school_limit

    def set_payment_history(self, new_history):
        self.payment_history = new_history

    def set_booking_history(self, new_history):
        self.booking_history = new_history

    def create_history(self, data, hour):
        """
        Creates an initial record in the booking history. 
        """
        history = self.booking_history
        number_of_seats = self._number_of_seats
        if data in history.keys():
            pass
        else:
            history[data] =\
                {hour: [number_of_seats, 0, []]}
        if hour in history[data]:
            pass
        else:
            x = [number_of_seats, 0, []]
            history[data][hour] = x

    def next_day(self, date):
        """
        Returns hour and date for next day.
        """
        (year, month, day) = date.split("-")
        date = datetime.date(int(year), int(month), int(day))
        date = str(date + datetime.timedelta(days=1))
        hour = self.get_work_hours()[0]
        return hour, date

    def get_free_tracks(self, date, hour):
        """
        Returns the number of free tracks for the given date and time.
        """
        self.create_history(date, hour)
        busy_tracks = self.booking_history[date][hour][1]
        all_tracks = self.get_number_of_tracks()
        return all_tracks - busy_tracks

    def get_free_seats(self, date, hour):
        """
        Returns the number of free seats for the given date and time.
        """
        self.create_history(date, hour)
        return self.booking_history[date][hour][0]

    def checking_free_seats(self, date, hour, number_of_reserved_seats):
        """
        Checks whether the given number of seats is available on a given day at a given time.
        """
        free_seats = self.get_free_seats(date, hour)
        number = number_of_reserved_seats
        if number <= 0:
            return False, number
        if number > free_seats:
            return None, number
        return True, number

    def looking_for_free_seats(self, date, hour, number_of_seats):
        """
        Search for the closest date on which the given number of seats is available.
        """
        work_hours = self.get_work_hours()
        while True:
            free_seats = self.get_free_seats(date, hour)
            if hour >= work_hours[1]:
                hour, date = self.next_day(date)
                self.create_history(date, hour)
                hour, date, number_of_seats = \
                    self.looking_for_free_seats(
                        date, hour, number_of_seats)
            free_seats = self.get_free_seats(date, hour)
            if free_seats >= number_of_seats:
                return hour, date, number_of_seats
            elif hour >= work_hours[0]:
                hour += 1
                self.create_history(date, hour)

    def checking_free_tracks(self, date, hour, number_of_reserved_tracks):
        """
        Checks whether the given number of tracks is available on a given day at a given time.
        """
        number = number_of_reserved_tracks
        condition = self.checking_swimming_schools_condition(
            number, date, hour)
        if not condition:
            return None, number
        free_tracks = self.get_free_tracks(date, hour)
        if number <= 0:
            return False, number
        is_free_seats, num = self.checking_free_seats(date, hour, PERSONPERTRACK*number)
        if not is_free_seats or is_free_seats is None:
            return None, number
        if number < free_tracks:
            return True, number
        return None, number

    def looking_for_free_tracks(self, date, hour, number_of_tracks):
        """
        Search for the closest date on which the given number of tracks is available.
        """
        work_hours = self.get_work_hours()
        while True:
            free_tracks = self.get_free_tracks(date, hour)
            condition, number_of_tracks = self.checking_free_tracks(
                date, hour, number_of_tracks)
            if hour >= work_hours[1]:
                hour, date = self.next_day(date)
                hour, date, number_of_tracks = \
                    self.looking_for_free_tracks(
                        date, hour, number_of_tracks)
            free_tracks = self.get_free_tracks(date, hour)
            condition, number_of_tracks = self.checking_free_tracks(
                date, hour, number_of_tracks)
            if free_tracks >= number_of_tracks and condition:
                return hour, date, number_of_tracks
            elif hour >= work_hours[0]:
                hour += 1
                self.create_history(date, hour)

    def checking_swimming_schools_condition(
            self, number_of_reserved_tracks, date, hour):
        """
        Checks whether the given number of tracks complies with the conditions of the swimming schools.
        """
        self.create_history(date, hour)
        number = self.get_number_of_tracks()
        if int(SCHOOLTRACKPARAMETER * number) >= number_of_reserved_tracks +\
                self.booking_history[date][hour][1]:
            return True
        return False

    def generate_payment_history(self, date):
        """
        Creates an initial record in the payment history. 
        """
        try:
            if self.payment_history[date]:
                pass
        except KeyError:
            self.payment_history[date] = 0

    def generate_payment(
            self, date, day_of_the_week,
            day_time, type_of_client,
            number_of_seats=0, number_of_tracks=0):
        """
        Generates a fee depending on the day of the week, time of day and type of customer.
        """
        try:
            self.payment_history[date]
        except KeyError:
            self.payment_history[date] = 0
        if type_of_client == "individual":
            number = number_of_seats
            self.generate_payment_history(date)
            price = self._price_list['client'][day_time][day_of_the_week]
            payment = number * price
            self.payment_history[date] += payment
            return payment
        elif type_of_client == "school":
            number = number_of_tracks
            self.generate_payment_history(date)
            price = self._price_list['school'][day_time][day_of_the_week]
            payment = number * price
            self.payment_history[date] += payment
            return payment
