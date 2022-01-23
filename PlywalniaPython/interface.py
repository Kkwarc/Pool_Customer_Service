# Startup file for the console interface.
import json
from datetime import date
from clients import IndividualCustomer, SwimmingSchool
from swimming_pool import SwimmingPool
from body import Body


def open_price_list():
    """
    Opens the file containing the price list and returns it.
    """
    with open("price_list.json", "r") as price_list:
        price_list = json.load(price_list)
    return price_list


def give_int_input(text):
    """
    Checks whether the given text is a number.
    """
    try:
        inp = int(input(text))
    except ValueError:
        print("Wrong input!")
        return False
    return inp


def entering_date(b):
    """
    Interacting with the user - getting the date.
    Date should be after todays date.
    """
    enter_date = ""
    date_now = date.today()
    while True:
        enter_date = input('Enter the date in the format yyyy-mm-dd: \n')
        enter_date = b.checking_time(enter_date)
        if not enter_date:
            print("\n####################\n")
            print("Wrong date")
            print(f'The date must be after {date_now}!')
            print('Enter the new date in the format yyyy-mm-dd: ')
            print("\n####################\n")
            continue
        if not b.checking_year_compared_to_now(enter_date):
            print("\n####################\n")
            print("Wrong date!")
            print('Enter the new date in the format yyyy-mm-dd: ')
            print("\n####################\n")
            continue
        return enter_date


def entering_date_with_no_year_limit(b):
    """
    Interacting with the user - getting the date.
    No limits for date.
    """
    enter_date = ""
    while True:
        enter_date = input('Enter the date in the format yyyy-mm-dd: \n')
        enter_date = b.checking_time(enter_date)
        if not enter_date:
            print("\n####################\n")
            print("Wrong date")
            print('Enter the new date in the format yyyy-mm-dd: ')
            print("\n####################\n")
            continue
        return enter_date


def entering_hour(b, sp):
    """
    Interacting with the user - getting the hour.
    """
    hour = 0
    while True:
        hour = give_int_input('Enter hour: \n')
        if hour is False:
            continue
        hour = b.checking_hour(sp, hour)
        if hour:
            return hour
        else:
            print("Enter correct hour!")


def accepting_new_date_client(sp, hour, date, number):
    """
    Communication of acceptance of the new date with client.
    """
    print("No free seats on a given date")
    hour, date, number = sp.looking_free_seats(
        date, hour, number)
    print(f"Earliest next date: {date} at {hour}")
    while True:
        inp = input("Do you accept[y/n]: ")
        if inp == "y" or inp == "Y":
            return date, hour, number
        elif inp == "n" or inp == "N":
            return None, None, None
        else:
            print("Wrong input")


def entering_number_of_seats(sp, date, hour):
    """
    Interacting with the user - getting the number of seats.
    """
    number = 0
    while True:
        number = give_int_input("Enter number of reserved seats: ")
        if number > sp.get_number_of_seats():
            print("You tried to exceeded the maximum number of seats!")
            print(f"Max number you can enter is {sp.get_number_of_seats()}")
            continue
        if number is False:
            continue
        is_free_seats, number = sp.checking_free_seats(date, hour, number)
        if is_free_seats is True:
            return date, hour, number
        elif is_free_seats is None:
            date, hour, number = accepting_new_date_client(sp, hour, date, number)
            if date is None:
                return None, None, None
            else:
                return date, hour, number
        elif is_free_seats is False:
            print("Enter correct number!")


def accepting_new_date_school(sp, hour, date, number):
    """
    Communication of acceptance of the new date with swimming school.
    """
    print("No free tracks on a given date")
    hour, date, number = sp.looking_free_tracks(
        date, hour, number)
    print(f"Earliest next date: {date} at {hour}")
    while True:
        inp = input("Do you accept[y/n]: ")
        if inp == "y" or inp == "Y":
            return date, hour, number
        elif inp == "n" or inp == "N":
            return None, None, None
        else:
            print("Wrong input")

def entering_number_of_tracks(sp, date, hour):
    """
    Interacting with the user - getting the number of tracks.
    """
    number = 0
    while True:
        number = give_int_input("Enter number of reserved tracks: ")
        limit = sp.get_swimming_pool_school_limit()
        if number > limit:
            print("You tried to exceeded the maximum number of tracks!")
            print(f"Max number you can enter is {limit}")
            continue
        is_free_tracks, number = sp.checking_free_tracks(date, hour, number)
        if is_free_tracks is True:
            return date, hour, number
        elif is_free_tracks is None:
            date, hour, number = accepting_new_date_school(sp, hour, date, number)
            if date is None:
                return None, None, None
            else:
                return date, hour, number
        elif is_free_tracks is False:
            print("Enter correct number!")


def check_book_history(sp, date):
    """
    Prints booking history for the given date.
    """
    print("\n####################\n")
    print("History on ", date, ":")
    for i in range(sp.get_work_hours()[0], sp.get_work_hours()[1] + 1):
        sp.create_history(date, i)
        print("Hour: ", i)
        print("Number of free seats: ", sp.booking_history[date][i][0])
        print("Number of reserved tracks: ", sp.booking_history[date][i][1])
        print("List of clients: ", sp.booking_history[date][i][2])
    print("\n####################\n")


def check_swimming_pool(sp):
    """
    Prints parameters of the swimming pool.
    """
    print("\n####################\n")
    print('Name:', sp.get_name())
    print(' Work hours:', sp.get_work_hours()[0], '-', sp.get_work_hours()[1])
    print(' Number of tracks:', sp.get_number_of_tracks())
    print(' Number of seats:', sp.get_number_of_seats())
    print("\n####################\n")


def financial_report(sp, b):
    """
    Prints the pool's earnings for the day.
    """
    date = entering_date_with_no_year_limit(b)
    sp.generate_payment_history(date)
    print("\n####################\n")
    print('The income on ', date, ' is ', sp.payment_history[date])
    print("\n####################\n")


def client_reserved(b, sp, i):
    """
    Interaction with client - reservation.
    """
    name = input("Enter name: ")
    date = entering_date(b)
    hour = entering_hour(b, sp)
    date, hour, number = entering_number_of_seats(sp, date, hour)
    if date is None:
        print("\n####################\n")
        print("Stopped!")
        print("\n####################\n")
        return 
    day_time = b.time_of_day(hour)
    day_of_the_week = b.get_day_of_the_week(date)
    sp.create_history(date, hour)
    payment, date, hour, number_of_seats = i.client_reserved(
        sp, date, hour, day_of_the_week, day_time, number, name)
    print("\n####################\n")
    print(f'Reserved {number} seats on {date} at {hour}')
    print(f'Payment is {payment} zl')
    print("\n####################\n")


def school_reserved(b, sp, ss):
    """
    Interaction with swimming school - reservation.
    """
    name = input("Enter name: ")
    date = entering_date(b)
    hour = entering_hour(b, sp)
    date, hour, number = entering_number_of_tracks(sp, date, hour)
    if date is None:
        print("\n####################\n")
        print("Stopped!")
        print("\n####################\n")
        return 
    day_time = b.time_of_day(hour)
    day_of_the_week = b.get_day_of_the_week(date)
    sp.create_history(date, hour)
    payment, date, hour, number_of_traks = ss.school_reserved(
        sp, date, hour, day_of_the_week, day_time, number, name)
    print("\n####################\n")
    print(f'Reserved {number} traks on {date} at {hour}')
    print(f'Payment is {payment} zl')
    print("\n####################\n")


def reserve_clients_menu():
    """
    Booking menu panel. 
    """
    options = {
        1: "client reserved",
        2: "school reserved",
        0: "no action"
        }
    while True:
        print("Do you want reserve individual customer[1]",
            "or swimming school[2] or come back[0]")
        user_input = give_int_input("Choose one of the options: ")
        if user_input is False:
            continue
        if user_input in options:
            return options[user_input]
        else:
            print("Wrong input!")


def main_menu():
    """
    Main menu panel. 
    """
    options = {
        0: "exit",
        2: "check booking history",
        3: "finacial report",
        4: "check swimming pool"
        }
    while True:
        print("Possible opcitons: ")
        print("Reserve[1]", "\nCheck booking history[2]",
            "Check financial raport[3]",
            "Check parameters of the swimming pool[4]", "\nexit[0]")
        user_input = give_int_input("Choose one of the options: ")
        if user_input is False:
            continue
        if user_input == 1:
            more_specific_user_input = reserve_clients_menu()
            if more_specific_user_input is False:
                continue
            if more_specific_user_input == "client reserved":
                return "client reserved"
            elif more_specific_user_input == "school reserved":
                return "school reserved"
            elif more_specific_user_input == "no action":
                return "no action"
            else:
                print("Wrong input!")
        if user_input in options:
            return options[user_input]
        else:
            print("Wrong input!")


def main():
    sp = SwimmingPool("Good Water", [8, 20], open_price_list(), 8)
    b = Body()
    i = IndividualCustomer("Customer")
    ss = SwimmingSchool("School")
    print("Hello there!")
    # Opening and loading files to the swimming pool.
    try:
        with open('payment_history.txt', 'r') as e:
            payment_history = json.load(e)
            sp.set_payment_history(payment_history)
    except json.decoder.JSONDecodeError:
        pass
    try:
        with open('booking_history.txt', 'r') as e:
            booking_history = json.load(e)
            sp.set_booking_history(booking_history)
    except json.decoder.JSONDecodeError:
        pass

    while True:
        x = main_menu()
        if x == "exit":
            print("Goodbye!")
            # Writing new data to files.
            with open('payment_history.txt', 'w') as e:
                json.dump(sp.payment_history, e, indent=4)
            with open('booking_history.txt', 'w') as e:
                json.dump(sp.booking_history, e, indent=4)
            break
        if x == "client reserved":
            client_reserved(b, sp, i)
        elif x == "school reserved":
            school_reserved(b, sp, ss)
        elif x == "check booking history":
            d = entering_date_with_no_year_limit(b)
            check_book_history(sp, d)
        elif x == "finacial report":
            financial_report(sp, b)
        elif x == "check swimming pool":
            check_swimming_pool(sp)
        elif x == "no action":
            print("\n####################\n")
        else:
            print("Wrong input!")
            continue

if __name__ == "__main__":
    main()