from loader import bot
from loguru import logger
from keyboards.reply.buttons import yes_or_no_button, currency, photo_count_keyboard
from states.user_data import UserInfoState
from telebot.types import Message, ReplyKeyboardRemove
from handlers.custom_handlers.calendar import calendar_command
from utils.api_request import search
from utils.api_request import city_markup


@bot.message_handler(commands=["custom"])
def custom(message: Message) -> None:
    """
    Обработчик команды custom. Запрашивает у пользователя город и осуществляет поиск с дополнительным
    пользовательским выбором цены и удалённости от центра.
    :param message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfoState.wait_city, message.chat.id)
    bot.send_message(message.from_user.id, f"{message.from_user.first_name}, вы выбрали команду для расширенного "
                                           f"поиска.Чтобы продолжить введите город",
                     reply_markup=ReplyKeyboardRemove())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        logger.info('Пользователь выбрал команду: ' + message.text + f" User_id: {message.chat.id}")
        data["command"] = message.text
        data["user_id"] = message.from_user.id


@bot.message_handler(state=UserInfoState.wait_city)
def custom_wait_city(message: Message) -> None:
    """
    Уточняем у пользователя при помощи клавиатуры в каком именно городе он хочет найти отель.
    :param message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    try:
        bot.send_message(message.from_user.id, "Уточните название города(custom)", reply_markup=city_markup(
            message.text))
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так, повторите попытку")
        bot.delete_state(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def custom_get_city(call) -> None:
    """
    Обрабатываем callback-запрос после нажатия пользователем на кнопку с городом и запоминаем выбранный город.
    :param call: Message
    :return: None
    """
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['city'] = call.data
            logger.info('Был выбран город: ' + call.data)
        custom_choice_currency(call)


def custom_choice_currency(call) -> None:
    """
    Обрабатываем выбор пользователем валюты для оплаты.
    :param call: Message
    :return: None
    """
    bot.send_message(call.from_user.id, f"Выбранный город: {call.data}. Выберите валюту:", reply_markup=currency())
    bot.set_state(call.from_user.id, UserInfoState.currency_selection, call.message.chat.id)


@bot.message_handler(state=UserInfoState.currency_selection)
def custom_get_night_price(message: Message) -> None:
    """
    Сохраняем выбранную валюту, и запрашиваем у пользователя минимальную цену проживания.
    Актуально только если пользователь выбрал команду custom.
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, f"Выбранная валюта: {message.text}. Введите минимальную цену",
                     reply_markup=ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, UserInfoState.price_min, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["currency"] = message.text
        logger.info(f"Выбрана валюта: {data['currency']}")


@bot.message_handler(state=UserInfoState.price_min)
def custom_get_price_range(message: Message) -> None:
    """
    Сохраняем минимальный прайс за проживание, и запрашиваем у пользователя максимальную цену проживания.
    Актуально только если пользователь выбрал команду custom.
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, f"Минимальная цена: {message.text}. "
                                           f"Введите максимальную цену.")
    bot.set_state(message.from_user.id, UserInfoState.price_max, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["price_min"] = message.text
        logger.info(f"Минимальный прайс за проживание: {data['price_min']}")


@bot.message_handler(state=UserInfoState.price_max)
def custom_get_price_range_max(message: Message) -> None:
    """
    Сохраняем максимальный прайс за проживание, и запрашиваем минимально желаемую отдалённость отеля от центра города.
    Актуально только если пользователь выбрал команду custom.
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, f"Максимальная цена: {message.text}. "
                                           f"Теперь введите минимальную отдалённость от центра (в км).")
    bot.set_state(message.from_user.id, UserInfoState.distance_min, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["price_max"] = message.text
        logger.info(f"Максимальный прайс за проживание: {data['price_max']}")


@bot.message_handler(state=UserInfoState.distance_min)
def custom_get_distance_range(message: Message) -> None:
    """
    Сохраняем минимальное расстояние от центра, и запрашиваем максимальную отдалённость отеля от центра города.
    Актуально только если пользователь выбрал команду custom.
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, f"Минимальное расстояние: {message.text}. "
                                           f"Введите максимальное расстояние от центра (в км).")
    bot.set_state(message.from_user.id, UserInfoState.distance_max, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["distance_min"] = message.text
        logger.info(f"Минимальное расстояние от центра: {data['distance_min']}")


@bot.message_handler(state=UserInfoState.distance_max)
def custom_get_distance_range_max(message: Message) -> None:
    """
    Сохраняем максимальное расстояние от центра, и запрашиваем у пользователя дату заезда при помощи календаря.
    Актуально только если пользователь выбрал команду custom.
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, f"Максимальное расстояние {message.text}. Выберите дату заезда")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["distance_max"] = message.text
        logger.info(f"Максимальное расстояние от центра: {data['distance_max']}")
    calendar_command(message)


@bot.message_handler(state=UserInfoState.count)
def custom_get_count(message: Message) -> None:
    """
    Сохраняем кол-во отелей и запрашиваем у пользователя нужны ли ему фото отелей при помощи кнопок."
    :param message: Message
    :return: None
    """""
    bot.send_message(message.from_user.id, f"Выбранное кол-во отелей: {message.text}. Нужны ли фото отелей?",
                     reply_markup=yes_or_no_button())
    bot.set_state(message.from_user.id, UserInfoState.photo_count, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["count"] = message.text
        logger.info(f"Выбрано кол-во отелей: {data['count']}")


@bot.message_handler(state=UserInfoState.photo_count)
def custom_get_photo_count(message: Message) -> None:
    """
    Если пользователю нужны фото, то уточняем их кол-во, иначе не предоставляем фото.
    :param message: Message
    :return: None
    """
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, 'Выберите кол-во фото на каждый отель',
                         reply_markup=photo_count_keyboard())
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
        logger.info("Фотографии отеля? Да!")
    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
        custom_get_photo(message)
        logger.info("Фотографии отеля? Нет!")


@bot.message_handler(state=UserInfoState.photo)
def custom_get_photo(message: Message) -> None:
    """
    Выводим всю собранную информацию в чат бота и выполняем поиск отелей.
    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, "Вы указали следующие параметры: ", reply_markup=ReplyKeyboardRemove())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["count_photo"] = message.text

    text = f"Город: {data['city']}\nДата заезда: {data['check_in']}\nДата выезда: {data['check_out']}\n" \
           f"Кол-во отелей: {data['count']}\nКол-во: {data['count_photo']}\n" \
           f"Диапазон расстояния: {data['distance_min']}-{data['distance_max']}\n" \
           f"Диапазон цен: {data['price_min']}-{data['price_max']}\n" \
           f"Команда: {data['command']}\n"
    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Выполняю поиск, пожалуйста, подождите...")
    search(message, data)
