from telebot.handler_backends import State, StatesGroup


class LowPriceInfoState(StatesGroup):
    wait_city = State()
    destination_id = State()
    city = State()
    currency_selection = State()
    count = State()
    photo_count = State()
    photo = State()


class HighPriceInfoState(StatesGroup):
    wait_city = State()
    city = State()
    currency_selection = State()
    count = State()
    photo_count = State()
    photo = State()


class UserInfoState(StatesGroup):
    wait_city = State()
    city = State()
    currency_selection = State()
    price_min = State()
    price_max = State()
    distance_min = State()
    distance_max = State()
    count = State()
    photo_count = State()
    photo = State()
    country = State()
    price_range = State()
    date = State()
    price_night = State()
    search = State()
    check_in = State()
    check_out = State()
    calendar = State()
    clean_history = State()


class DateRangeState(StatesGroup):
    check_in = State
    check_out = State


