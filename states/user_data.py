from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_number = State()
    count = State()
    photo = State()
    price_range = State()
    distance_min = State()
    distance_max = State()
    date = State()
    price_night = State()
    search = State()
    wait_city = State()
    currency_selection = State()
    check_in = State()
    check_out = State()
    calendar = State()
    price_min = State()
    price_max = State()
    photo_count = State()
    clean_history = State()


class DateRangeState(StatesGroup):
    check_in = State
    check_out = State



