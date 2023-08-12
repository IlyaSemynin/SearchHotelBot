from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    input_city = State()  # город, который ввёл пользователь
    check_city = State()  # выбор города из предложенных вариантов
    price_min = State()  # минимальная цена
    price_max = State()  # максимальная цена
    distance_min = State()
    distance_max = State()
    check_in = State()
    check_out = State()
    count_hotel = State()  # количество отелей
    count_photos = State()
    info = State()


