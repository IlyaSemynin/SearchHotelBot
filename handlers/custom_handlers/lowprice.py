from loader import bot
from loguru import logger
from keyboards.reply.buttons import yes_or_no_button, currency, photo_count_keyboard
from states.user_data import UserInfoState
from telebot.types import Message, ReplyKeyboardRemove
from handlers.custom_handlers.calendar import calendar_command
from handlers.custom_handlers.api_request import search
from handlers.custom_handlers.api_request import city_markup


@bot.message_handler(commands=["low"])
def low_price(message: Message) -> None:
    """
    Обработчик команды low. Запрашивает у пользователя город для поиска отелей
    :param message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfoState.wait_city, message.chat.id)
    bot.send_message(message.from_user.id, f"{message.from_user.first_name},вы выбрали команду для поиска "
                                           f"бюджетных отелей. Чтобы продолжить введите город",
                     reply_markup=ReplyKeyboardRemove())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data.clear()
        logger.info('Пользователь выбрал команду: ' + message.text + f" User_id: {message.chat.id}")
        data["command"] = message.text
        data["user_id"] = message.from_user.id


@bot.message_handler(state=UserInfoState.wait_city)
def wait_city(message: Message) -> None:
    """
    Уточняем, в каком именно городе пользователь хочет найти отель при помощи клавиатуры

    :param message: Message
    :return: None
    """
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    try:
        bot.send_message(message.from_user.id, "Уточните название города:", reply_markup=city_markup(message.text))
    except:
        bot.send_message(message.from_user.id, "Что-то пошло не так, повторите попытку")
        bot.delete_state(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def get_city(call) -> None:
    """
    Обрабатываем callback-запрос после нажатия пользователем на кнопку с городом и запоминаем выбранный город
    :param call: Message
    :return: None
    """
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['city'] = call.data
            logger.info('Был выбран город: ' + call.data)
        choice_currency(call)


def choice_currency(call) -> None:
    """
    Обрабатываем выбор пользователем валюты для оплаты
    :param call: Message
    :return: None
    """
    bot.send_message(call.from_user.id, f"Выбранный город: {call.data}. Выберите валюту:", reply_markup=currency())
    bot.set_state(call.from_user.id, UserInfoState.currency_selection, call.message.chat.id)


@bot.message_handler(state=UserInfoState.currency_selection)
def get_night_price(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["currency"] = message.text
        logger.info('Выбрана валюта: ' + data["currency"])
    bot.send_message(message.from_user.id, f"Выбранная валюта: {message.text}. Выберите дату заезда:",
                     reply_markup=ReplyKeyboardRemove())
    calendar_command(message)


@bot.message_handler(state=UserInfoState.count)
def get_count(message: Message) -> None:
    bot.send_message(message.from_user.id, f"Выбранное кол-во отелей: {message.text}. Нужны ли фото отелей?",
                     reply_markup=yes_or_no_button())
    bot.set_state(message.from_user.id, UserInfoState.photo_count, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["count"] = message.text
        logger.info(f"Выбрано кол-во отелей: {data['count']}")


@bot.message_handler(state=UserInfoState.photo_count)
def get_photo_count(message: Message) -> None:
    if message.text.lower() == 'да':
        bot.send_message(message.from_user.id, 'Выберите кол-во фото на каждый отель',
                         reply_markup=photo_count_keyboard())
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
        logger.info("Фотографии отеля? Да!")
    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserInfoState.photo, message.chat.id)
        get_photo(message)
        logger.info("Фотографии отеля? Нет!")


@bot.message_handler(state=UserInfoState.photo)
def get_photo(message: Message) -> None:
    bot.send_message(message.from_user.id, "Вы указали следующие параметры: ", reply_markup=ReplyKeyboardRemove())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["count_photo"] = message.text
        logger.info(f"Выбрано кол-во фото: {data['count_photo']}")
    text = f"Город: {data['city']}\nДата заезда: {data['check_in']}\nДата выезда: {data['check_out']}\n" \
           f"Кол-во отелей: {data['count']}\nКол-во фото: {data['count_photo']}\nКоманда: {data['command']}\n"
    bot.send_message(message.from_user.id, text)
    bot.send_message(message.from_user.id, "Выполняю поиск, пожалуйста подождите...")
    search(message, data)

