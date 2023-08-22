from loader import bot
from states.user_data import UserInfoState
from telebot.types import Message
from handlers.custom_handlers.calendar import calendar_command


@bot.message_handler(state=UserInfoState.price_min)
def get_price_range(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Минимальная цена: {message.text}. "
                                           f"Введите максимальную цену.")
    bot.set_state(message.from_user.id, UserInfoState.price_max, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["price_min"] = message.text


@bot.message_handler(state=UserInfoState.price_max)
def get_price_range(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Максимальная цена: {message.text}. "
                                           f"Теперь введите минимальное расстояние от центра в киллометрах.")
    bot.set_state(message.from_user.id, UserInfoState.distance_min, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["price_max"] = message.text


@bot.message_handler(state=UserInfoState.distance_min)
def get_distance_range(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Минимальное расстояние: {message.text}. "
                                           f"Введите максимальное расстояние от центра в киллометрах.")
    bot.set_state(message.from_user.id, UserInfoState.distance_max, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["distance_min"] = message.text


@bot.message_handler(state=UserInfoState.distance_max)
def get_distance_range(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Максимальное расстояние {message.text}. Выберите дату заезда")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["distance_max"] = message.text
    calendar_command(message)