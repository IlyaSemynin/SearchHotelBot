from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def count_hotel_button() -> ReplyKeyboardMarkup:
    """Кнопки для кол-ва выводимых отелей"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('1'))
    keyboard.add(KeyboardButton('2'))
    keyboard.add(KeyboardButton('3'))
    keyboard.add(KeyboardButton('4'))
    keyboard.add(KeyboardButton('5'))
    return keyboard


def yes_or_no_button() -> ReplyKeyboardMarkup:
    """Кнопки 'Да' и 'Нет'"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton("Да"))
    keyboard.add(KeyboardButton("Нет"))
    return keyboard


def currency() -> ReplyKeyboardMarkup:
    """Кнопки выбора валюты"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("USD")))
    keyboard.add((KeyboardButton("EUR")))
    return keyboard


def photo_count_keyboard() -> ReplyKeyboardMarkup:
    """Кнопки кол-ва фото отелей"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("1")))
    keyboard.add((KeyboardButton("2")))
    keyboard.add((KeyboardButton("3")))
    keyboard.add((KeyboardButton("4")))
    keyboard.add((KeyboardButton("5")))
    return keyboard


def delete_history() -> ReplyKeyboardMarkup:
    """Кнопка для очистки истории"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("❌Очистить историю❌")))
    return keyboard

