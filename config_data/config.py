import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("low", "Показать бюджетные отели в городе"),
    ("high", "Показать дорогие отели в городе"),
    ("custom", "Показать отели в пользовательском диапазоне"),
    ("history", "Показать историю запросов пользователя"),
)

HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
}

PAYLOAD = {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
}
