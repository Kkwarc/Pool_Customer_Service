from swimmingpool_parameters import PERSONPERTRACK


class IndividualCustomer:
    """
    Class: Individual customer
    Has: name
    Contains the method of booking seats for a given swimming pool.
    """
    def __init__(self, name: str):
        self.name = name

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def reserved(self, sp, data, hour, number_of_seats, name):
        """
        Record reservation data in history.
        """
        sp.booking_history[data][hour][0] -= number_of_seats
        sp.booking_history[data][hour][2].append(name)

    def client_reserved(
            self, sp, date, hour, day_of_the_week, day_time,
            number_of_seats, name):
        """
        Reservation and payment.
        """
        self.reserved(sp, date, hour, number_of_seats, name)
        payment = sp.generate_payment(
            date, day_of_the_week, day_time, "individual", number_of_seats
            )
        return payment, date, hour, number_of_seats


class SwimmingSchool(IndividualCustomer):
    """
    Class: Swimming school
    Inherits from Individual customer
    Has: name
    Contains the method of booking tracks for a given swimming pool.
    """
    def __init__(self, name: str):
        super().__init__(name)

    def reserved(self, sp, data, hour, number_of_tracks, name):
        """
        Record reservation data in history.
        """
        sp.booking_history[data][hour][0] -= number_of_tracks * PERSONPERTRACK
        sp.booking_history[data][hour][1] += number_of_tracks
        sp.booking_history[data][hour][2].append(name)

    def school_reserved(
        self, sp, date, hour, day_of_the_week, day_time, number_of_tracks, name
            ):
        """
        Reservation and payment.
        """
        self.reserved(sp, date, hour, number_of_tracks, name)
        payment = sp.generate_payment(
            date, day_of_the_week, day_time, "school", 0, number_of_tracks
            )
        return payment, date, hour, number_of_tracks
