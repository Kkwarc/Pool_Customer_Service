import clients
import swimming_pool
import body
import json


def open_price_list():
    with open("price_list.json", "r") as price_list:
        price_list = json.load(price_list)
    return price_list


price_list = open_price_list()


# test swimming pool
def test_create_swimming_pool():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.get_name() == "name"
    assert s.get_work_hours() == [8, 20]
    assert s.get_number_of_seats() == 25
    assert s.get_number_of_tracks() == 5
    assert s.booking_history == {}
    assert s.payment_history == {}


def test_swimming_pool_next_day():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.next_day("2022-02-02")[0] == 8
    assert s.next_day("2022-02-02")[1] == "2022-02-03"


def test_swimming_pool_create_history_if_not_exist():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.create_history("2022-02-02", 10)
    ss = clients.SwimmingSchool("name")
    ss.reserved(s, "2022-02-02", 10, 1, "name")
    s.create_history("2022-02-02", 10)
    assert s.booking_history["2022-02-02"][10][0] == 20
    assert s.booking_history["2022-02-02"][10][1] == 1
    assert s.booking_history["2022-02-02"][10][2] == ["name"]


def test_swimming_pool_create_history_if_exist():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.create_history("2022-02-02", 10)
    assert s.booking_history["2022-02-02"][10][0] == 25
    assert s.booking_history["2022-02-02"][10][1] == 0
    assert s.booking_history["2022-02-02"][10][2] == []


def test_swimming_pool_get_free_tracks():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.get_free_tracks("2022-02-02", 10) == 5


def test_swimming_pool_get_free_tracks_after_school_reserved():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    ss = clients.SwimmingSchool("name")
    s.create_history("2022-02-02", 10)
    ss.reserved(s, "2022-02-02", 10, 1, "name")
    assert s.get_free_tracks("2022-02-02", 10) == 4


def test_swimming_pool_get_free_seats():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.get_free_seats("2022-02-02", 10) == 25


def test_swimming_pool_get_free_seats_after_client_reserved():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    c = clients.IndividualCustomer("name")
    s.create_history("2022-02-02", 10)
    c.reserved(s, "2022-02-02", 10, 3, "name")
    assert s.get_free_seats("2022-02-02", 10) == 22


def test_swimming_pool_checking_free_seasts():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.checking_free_seats("2022-02-02", 10, 10)[0] == 1
    assert s.checking_free_seats("2022-02-02", 10, 10)[1] == 10


def test_swimming_pool_checking_free_seasts_too_many_seats():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.checking_free_seats("2022-02-02", 10, 40)[0] is None
    assert s.checking_free_seats("2022-02-02", 10, 40)[1] == 40


def test_swimming_pool_checking_free_seasts_negative():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.checking_free_seats("2022-02-02", 10, -10)[0] is False
    assert s.checking_free_seats("2022-02-02", 10, -10)[1] == -10


def test_swimming_pool_looking_next_free_seats():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    c = clients.IndividualCustomer("name")
    s.create_history("2022-02-02", 10)
    c.reserved(s, "2022-02-02", 10, 25, "name")
    assert s.looking_for_free_seats("2022-02-02", 10, 5)[0] == 11
    assert s.looking_for_free_seats("2022-02-02", 10, 5)[1] == "2022-02-02"
    assert s.looking_for_free_seats("2022-02-02", 10, 5)[2] == 5


def test_swimming_pool_looking_next_free_seats_next_day():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    c = clients.IndividualCustomer("name")
    s.create_history("2022-02-02", 19)
    c.reserved(s, "2022-02-02", 19, 25, "name")
    assert s.looking_for_free_seats("2022-02-02", 19, 5)[0] == 8
    assert s.looking_for_free_seats("2022-02-02", 19, 5)[1] == "2022-02-03"
    assert s.looking_for_free_seats("2022-02-02", 19, 5)[2] == 5


def test_swimming_pool_looking_next_free_tracks():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    ss = clients.SwimmingSchool("name")
    s.create_history("2022-02-02", 10)
    ss.reserved(s, "2022-02-02", 10, 1, "name")
    assert s.looking_for_free_tracks("2022-02-02", 10, 1)[0] == 11
    assert s.looking_for_free_tracks("2022-02-02", 10, 1)[1] == "2022-02-02"
    assert s.looking_for_free_tracks("2022-02-02", 10, 1)[2] == 1


def test_swimming_pool_looking_next_free_tracks_next_day():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    ss = clients.SwimmingSchool("name")
    s.create_history("2022-02-02", 19)
    ss.reserved(s, "2022-02-02", 19, 1, "name")
    assert s.looking_for_free_tracks("2022-02-02", 19, 1)[0] == 8
    assert s.looking_for_free_tracks("2022-02-02", 19, 1)[1] == "2022-02-03"
    assert s.looking_for_free_tracks("2022-02-02", 19, 1)[2] == 1


def test_swimming_pool_checking_swimming_pool_condition():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.create_history("2022-02-02", 10)
    assert s. checking_swimming_schools_condition(1, "2022-02-02", 10) is True


def test_swimming_pool_checking_swimming_pool_condition_negative():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.create_history("2022-02-02", 10)
    assert s. checking_swimming_schools_condition(2, "2022-02-02", 10) is False


def test_swimming_pool_checking_free_tracks():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.checking_free_tracks("2022-02-02", 10, 1)[0] == 1
    assert s.checking_free_tracks("2022-02-02", 10, 1)[1] == 1


def test_swimming_pool_checking_free_tracks_too_many_seats():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.checking_free_tracks("2022-02-02", 10, 3)[0] is None
    assert s.checking_free_tracks("2022-02-02", 10, 3)[1] == 3


def test_swimming_pool_checking_free_tracks_negative():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert s.checking_free_tracks("2022-02-02", 10, -1)[0] is False
    assert s.checking_free_tracks("2022-02-02", 10, -1)[1] == -1


def test_swimming_pool_generate_payment_hisory_if_not_exist():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.generate_payment_history("2022-02-02")
    assert s.payment_history["2022-02-02"] == 0


def test_swimming_pool_generate_payment_hisory_if_exist():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.payment_history["2022-02-02"] = 10
    s.generate_payment_history("2022-02-02")
    assert s.payment_history["2022-02-02"] == 10


def test_swimming_pool_generate_payment_individual():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.generate_payment("2022-02-02", "Mon", "before_noon", "individual", 1)
    assert s.payment_history["2022-02-02"] == 10


def test_swimming_pool_generate_payment_school():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    s.generate_payment("2022-02-02", "Mon", "before_noon", "school", 0, 1)
    assert s.payment_history["2022-02-02"] == 40


# test customer
def test_create_customer():
    c = clients.IndividualCustomer("name")
    assert c.get_name() == "name"


def test_customer_reserved():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    c = clients.IndividualCustomer("name")
    s.create_history("2022-02-02", 10)
    c.reserved(s, "2022-02-02", 10, 3, "name")
    assert s.booking_history["2022-02-02"][10][0] == 22
    assert s.booking_history["2022-02-02"][10][1] == 0
    assert s.booking_history["2022-02-02"][10][2] == ["name"]


# test school
def test_create_school():
    ss = clients.SwimmingSchool("name")
    assert ss.get_name() == "name"


def test_school_reserved():
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    ss = clients.SwimmingSchool("name")
    s.create_history("2022-02-02", 10)
    ss.reserved(s, "2022-02-02", 10, 2, "name")
    assert s.booking_history["2022-02-02"][10][0] == 15
    assert s.booking_history["2022-02-02"][10][1] == 2
    assert s.booking_history["2022-02-02"][10][2] == ["name"]


# test body
def test_body_get_day_of_week():
    b = body.Body()
    assert b.get_day_of_the_week("2021-11-21") == "Sun"
    assert b.get_day_of_the_week("2021-11-22") == "Mon"


def test_body_checking_structure_date():
    b = body.Body()
    assert b.checking_structure_date("2021-11-21")[0] == 2021
    assert b.checking_structure_date("2021-11-21")[1] == 11
    assert b.checking_structure_date("2021-11-21")[2] == 21


def test_body_checking_date_failure():
    b = body.Body()
    assert b.checking_structure_date("fgarg") is False


def test_body_checking_date():
    b = body.Body()
    assert b.checking_date(2022, 11, 11) is True


def test_body_checking_date_month_error():
    b = body.Body()
    assert b.checking_date(2022, 13, 11) is False
    assert b.checking_date(2022, 0, 11) is False
    assert b.checking_date(2022, -1, 11) is False


def test_body_checking_date_day_error():
    b = body.Body()
    assert b.checking_date(2022, 12, 32) is False
    assert b.checking_date(2022, 12, 0) is False
    assert b.checking_date(2022, 12, -1) is False


def test_body_checking_year_compared_to_now():
    b = body.Body()
    assert b.checking_year_compared_to_now("2022-02-02") is True


def test_body_checking_yesr_compared_to_now_error():
    b = body.Body()
    assert b.checking_year_compared_to_now("2020-02-02") is False


def test_body_checking_time():
    b = body.Body()
    assert b.checking_time("2022-02-02") == "2022-02-02"


def test_body_checking_time_error():
    b = body.Body()
    assert b.checking_time("2022-20-02") is False
    assert b.checking_time("2022-02-32") is False


def test_body_checking_hour():
    b = body.Body()
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert b.checking_hour(s, 10) == 10
    assert b.checking_hour(s, 8) == 8
    assert b.checking_hour(s, 19) == 19


def test_body_checking_hour_error():
    b = body.Body()
    s = swimming_pool.SwimmingPool("name", [8, 20], price_list, 5)
    assert b.checking_hour(s, 21) is False
    assert b.checking_hour(s, 25) is False
    assert b.checking_hour(s, 7) is False
    assert b.checking_hour(s, -1) is False


def test_body_checking_time_of_day():
    b = body.Body()
    assert b.time_of_day(1) == "before_noon"
    assert b.time_of_day(11) == "before_noon"
    assert b.time_of_day(12) == "after_noon"
    assert b.time_of_day(23) == "after_noon"
