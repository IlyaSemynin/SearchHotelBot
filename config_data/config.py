import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("Пока не получил")
RAPID_API_KEY = os.getenv("7d177ea33dmsh040b70cdab9fabep1a1f4djsn4fc417c5c7d8")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку")
)
