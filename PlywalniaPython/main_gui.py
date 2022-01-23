# Startup file for the graphic interface.
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QListWidgetItem
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtGui import QFont
from ui_main import Ui_MainWindow
from ui_dialog import Ui_Dialog
from ui_dialog_enter_data import Ui_Dialog_Enter_Data
from ui_dialog_yes_no import Ui_Dialog_Yes_No

import json
import datetime

from clients import IndividualCustomer, SwimmingSchool
from swimming_pool import SwimmingPool
from body import Body
from gui_start_text import TEXT


def open_price_list():
    """
    Opens the file containing the price list and returns it.
    """
    with open("price_list.json", "r") as price_list:
        price_list = json.load(price_list)
    return price_list


class ReserveClientDialog(QDialog):
    """
    Class: Reserve Client Dialog
    Inherits from QDialog
    Makes a window in which user enters data for reservation and then checks this data.
    """
    def __init__(self, SwimmingPool, Body, IndyvidualCustomer, SwimmingSchool, parent=None):
        super().__init__(parent)
        self._sp = SwimmingPool
        self._b = Body
        self._i = IndyvidualCustomer
        self._ss = SwimmingSchool
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # connect button with function
        self.ui.addButton.clicked.connect(self.addData)
        # set hour limit
        self.ui.hour.setMinimum(self._sp.get_work_hours()[0])
        self.ui.hour.setMaximum(self._sp.get_work_hours()[1])
        # set set number limit
        limit = self._sp.get_number_of_seats()
        self.ui.number.setMaximum(limit)
        text_hour = f"Hour should be between {self._sp.get_work_hours()[0]}-{self._sp.get_work_hours()[1]}"
        text = f"Enter name: \nChoose date from calendar view: \nEnter hour({text_hour}): \nEnter number of seats to be reserved(max {limit}): \n"
        self.ui.View.setText(text)
        self._name = ""
        self._date = ""
        self._hour = 0
        self._number = 0

    def get_name(self):
        return self._name

    def get_date(self):
        return self._date

    def get_hour(self):
        return self._hour

    def get_number(self):
        return self._number

    def ui_get_name(self):
        """
        Loads text from "name field"
        And checks if it isn't empty.
        """
        enter_name = self.ui.name.text()
        if enter_name:
            self._name = enter_name
            return enter_name
        else:
            self.ui.View.setText("Name cannot be empty!")
            return None

    def ui_get_date(self):
        """
        Loads date from calendar
        And changes its format to str.
        """
        date_now = datetime.date.today()
        # convert data object to str
        enter_date = self.ui.date.selectedDate().toString(Qt.ISODate)
        self._date = enter_date
        return enter_date


    def ui_get_hour(self):
        """
        Loads hour from "hour field"
        And checks if it is correct.
        """
        enter_hour = int(self.ui.hour.text())
        self._hour = enter_hour
        return enter_hour

    def yes_no_dialog(self, name, date, hour, number):
        """
        Shows new window for user to accept new data.
        """
        text = "\nPress OK to continue"
        dialog = YesNoDialog(self)
        if dialog.exec_():
            choise = dialog.get_choise()
            if choise is True:
                self._name = name
                self._date = date
                self._hour = hour
                self._number = number
                self.ui.View.setText(f"Name: {name}\nDate: {date}\nHour: {hour}\nNumber: {number}" + text)
                return number
            elif choise is False:
                self.ui.View.setText("OK")
                self._name = None
                return None
            else:
                self.ui.View.setText("Wrong input!")

    def ui_get_number(self, enter_name, enter_date, enter_hour):
        """
        Loads and checks number of seats.
        If there is not enough on a given date, searches for a new possible date.
        """
        text = "\nPress OK to continue"
        enter_number = int(self.ui.number.text())
        is_free_seats, enter_number = self._sp.checking_free_seats(enter_date, enter_hour, enter_number)
        if is_free_seats is True:
            self._number = int(enter_number)
            self.ui.View.setText(f"Name: {enter_name}\nDate: {enter_date}\nHour: {enter_hour}\nNumber: {enter_number}" + text)
            return enter_number
        elif is_free_seats is None:
            text7 = "No free seats on a given date\n"
            self.ui.View.setText(text + text7)
            # looking for next possible date
            hour, date, number = self._sp.looking_free_seats(
                enter_date, enter_hour, enter_number)
            text8 = f"Earliest next date: {date} at {hour}"
            self.ui.View.setText(text7 + text8)
            # shows new window to accept or reject new date
            number = self.yes_no_dialog(enter_name, date, hour, number)
            if number is None:
                return
            else:
                return number
        elif is_free_seats is False:
            text10 = "Enter correct number!"
            self.ui.View.setText(text10)
            return None

    def addData(self):
        #name
        enter_name = self.ui_get_name()
        if enter_name is None:
            return

        #date
        enter_date = self.ui_get_date()
        if enter_date is None:
            return

        #hour
        enter_hour = self.ui_get_hour() 
        if enter_hour is None:
            return

        #number
        if self.ui_get_number(enter_name, enter_date, enter_hour) is None:
            return


class ReserveSchoolDialog(ReserveClientDialog):
    """
    Class: Reserve Client Dialog
    Inherits from Reserve Cilient Dialog
    Makes a window in which user enter data for reservation
    And checks this data.
    """
    def __init__(self, SwimmingPool, Body, IndividualCustomer, SwimmingSchool, parent=None):
        super().__init__(SwimmingPool, Body, IndividualCustomer, SwimmingSchool, parent)
        # set set number limit
        limit = self._sp.get_swimming_pool_school_limit()
        self.ui.number.setMaximum(limit)
        text_hour = f"Hour should be between {self._sp.get_work_hours()[0]}-{self._sp.get_work_hours()[1]}"
        text = f"Enter name: \nChoose date from calendar view: \nEnter hour({text_hour}): \nEnter number of tracks to be reserved(max {limit}): \n"
        self.ui.View.setText(text)

    def ui_get_number(self, enter_name, enter_date, enter_hour):
        """
        Loads and checks number of tracks.
        If there is not enough on a given date, searches for a new possible date.
        """
        text = "\nPress OK to continue"
        enter_number = int(self.ui.number.text())
        is_free_tracks, enter_number = self._sp.checking_free_tracks(enter_date, enter_hour, enter_number)
        if is_free_tracks is True:
            self._number = int(enter_number)
            self.ui.View.setText(f"Name: {enter_name}\nDate: {enter_date}\nHour: {enter_hour}\nNumber: {enter_number}" + text)
            return enter_number
        elif is_free_tracks is None:
            text7 = "No free tracks on a given date\n"
            self.ui.View.setText(text + text7)
            # looking for next possible date
            hour, date, number = self._sp.looking_for_free_tracks(
                enter_date, enter_hour, enter_number)
            text8 = f"Earliest next date: {date} at {hour}"
            self.ui.View.setText(text7 + text8)
            # shows new window to accept or reject new date
            number = self.yes_no_dialog(enter_name, date, hour, number)
            if number is None:
                return None
            else:
                self.ui.View.setText(f"Name: {enter_name}\nDate: {date}\nHour: {hour}\nNumber: {number}" + text)
                return number
        elif is_free_tracks is False:
            text10 = "Enter correct number!"
            self.ui.View.setText(text10)
            return None


class DateDialog(QDialog):
    """
    Class: Date Dialog
    Inherits from QDialog
    Makes a window in which user enters data
    Then it checks this data.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_ui = Ui_Dialog_Enter_Data()
        self.data_ui.setupUi(self)
        self.data_ui.addButton.clicked.connect(self.addDate)
        self.data_ui.View.setText("Choose date from calendar view: ")
        self._date = ""

    def addDate(self):
        """
        Loads and checks data.
        """
        date_now = datetime.date.today()
        # convert data object to str
        enter_date = self.data_ui.date.selectedDate().toString(Qt.ISODate)
        self.data_ui.View.setText("Choose date from calendar view: " + str(enter_date))
        self._date = enter_date

    def get_date(self):
        return self._date


class YesNoDialog(QDialog):
    """
    Class: Yes No Dialog
    Inherits from QDialog
    Makes a window in which user accept or reject new data.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.YN_ui = Ui_Dialog_Yes_No()
        self.YN_ui.setupUi(self)
        # connect button with function
        self.YN_ui.addYesButton.clicked.connect(self.set_Yes)
        self.YN_ui.addNoButton.clicked.connect(self.set_No)
        self.text1 = "Do you accept?\n"
        self.YN_ui.View.setText(self.text1)
        self._choise = None

    def set_Yes(self):
        """
        User accepts data
        """
        self._choise = True
        self.YN_ui.View.setText(self.text1 + "Yes")

    def set_No(self):
        """
        User rejects data
        """
        self._choise = False
        self.YN_ui.View.setText(self.text1 + "No")

    def get_choise(self):
        return self._choise

class MainWindow(QMainWindow):
    """
    Class: Main Window
    Inherits from QMainWindow
    Makes a window in which program interacts with user.
    And have menu bar in which user can choose
    what they want to do in program:
    Reserve client / school
    Show booking history / payment history
    Load from/ Save to file
    """
    def __init__(self, SwimmingPool, Body, IndividualCustomer, SwimmingSchool, parent=None):
        super().__init__(parent)
        self._sp = SwimmingPool
        self._b = Body
        self._i = IndividualCustomer
        self._ss = SwimmingSchool
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # connect buttons with functions
        self.ui.actionAddReservation.triggered.connect(self.addClientReservation)
        self.ui.actionAddReservation2.triggered.connect(self.addSchoolReservation)
        self.ui.actionAddDate.triggered.connect(self.addDataCheckBookingHistory)
        self.ui.actionAddDate2.triggered.connect(self.addDataCheckFinancialRaport)
        self.ui.actionLoad.triggered.connect(self.LoadFromFile)
        self.ui.actionSave.triggered.connect(self.SaveToFile)
        self.ui.menuStartScreen.triggered.connect(self.ShowStartScreen)
        text = ""
        # font enlargement
        self.ui.View.setFont(QFont(text, 10))
        self.ui.View.setText(TEXT)

    def LoadFromFile(self):
        """
        Loads data from files
        if file does not exist - pass.
        """
        try:
            with open('payment_history.txt', 'r') as e:
                payment_history = json.load(e)
                self._sp.set_payment_history(payment_history)
                self.ui.View.setText("Loaded")
        except json.decoder.JSONDecodeError:
            pass
        try:
            with open('booking_history.txt', 'r') as e:
                booking_history = json.load(e)
                self._sp.set_booking_history(booking_history)
                self.ui.View.setText("Loaded")
        except json.decoder.JSONDecodeError:
            pass

    def SaveToFile(self):
        """
        Save data to files.
        """
        with open('payment_history.txt', 'w') as e:
            json.dump(self._sp.payment_history, e, indent=4)
            self.ui.View.setText("Saved")
        with open('booking_history.txt', 'w') as e:
            json.dump(self._sp.booking_history, e, indent=4)
            self.ui.View.setText("Saved")

    def ShowStartScreen(self):
        """
        Show start screen.
        """
        self.ui.View.setText(TEXT)

    def addClientReservation(self):
        """
        Interaction with client - reservation.
        """
        dialog = ReserveClientDialog(self._sp, self._b, self._i, self._ss)
        if dialog.exec_():
            name = dialog.get_name()
            date = dialog.get_date()
            hour = dialog.get_hour()
            number = dialog.get_number()
            if name is None:
                self.ui.View.setText("Reservation stopped!")
            elif name == "" or date == "" or hour <= 0 or number <= 0:
                self.ui.View.setText("An error occurred while entering the data!")
            else:
                day_of_the_week = self._b.get_day_of_the_week(date)
                day_time = self._b.time_of_day(hour)
                self._sp.create_history(date, hour)
                payment, date, hour, number_of_traks = self._i.client_reserved(
                    self._sp, date, hour, day_of_the_week, day_time, number, name)
                text1 = f'Reserved {number} seats on {date} at {hour}\n'
                text2 = f'Payment is {payment} zl'
                self.ui.View.setText(text1 + text2)

    def addSchoolReservation(self):
        """
        Interaction with swimming school - reservation.
        """
        dialog = ReserveSchoolDialog(self._sp, self._b, self._i, self._ss)
        if dialog.exec_():
            name = dialog.get_name()
            date = dialog.get_date()
            hour = dialog.get_hour()
            number = dialog.get_number()
            if name is None:
                self.ui.View.setText("Reservation stopped!")
            elif name == "" or date == "" or hour <= 0 or number <= 0:
                self.ui.View.setText("An error occurred while entering the data!")
            else:
                day_of_the_week = self._b.get_day_of_the_week(date)
                day_time = self._b.time_of_day(hour)
                self._sp.create_history(date, hour)
                payment, date, hour, number_of_traks = self._ss.school_reserved(
                    self._sp, date, hour, day_of_the_week, day_time, number, name)
                text = f'Reserved {number} traks on {date} at {hour}\nPayment is {payment} zl'
                self.ui.View.setText(text)

    def addDataCheckFinancialRaport(self):
        """
        Interaction with user - show reservation history.
        """
        dialog = DateDialog(self)
        if dialog.exec_():
            date = dialog.get_date()
            if not date:
                self.ui.View.setText("An error occurred while entering the date!")
            else:
                self._sp.generate_payment_history(date)
                text = 'The income on ' + date + ' is ' + str(self._sp.payment_history[date])
                self.ui.View.setText(text)

    def addDataCheckBookingHistory(self):
        """
        Interaction with user - show booking history.
        """
        dialog = DateDialog(self)
        if dialog.exec_():
            date = dialog.get_date()
            if not date:
                self.ui.View.setText("An error occurred while entering the date!")
            else:
                text = "History on " + date + ":\n"
                for i in range(self._sp.get_work_hours()[0], self._sp.get_work_hours()[1] + 1):
                    self._sp.create_history(date, i)
                    text += "Hour: " + str(i) + "\n"
                    text += "Number of free seats: " + str(self._sp.booking_history[date][i][0]) + "\n"
                    text += "Number of reserved tracks: " + str(self._sp.booking_history[date][i][1]) + "\n"
                    text += "List of clients: " + str(self._sp.booking_history[date][i][2]) + "\n"
                self.ui.View.setText(text)


def main():
    sp = SwimmingPool("Good Water", [8, 20], open_price_list(), 8)
    b = Body()
    i = IndividualCustomer("Customer")
    ss = SwimmingSchool("School")
    app = QApplication([])
    window = MainWindow(sp, b, i, ss)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
