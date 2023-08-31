# Подгружаем необходимые модули для создания бота
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config

#  Создаем глобальную переменную для хранения состояний пользователя внутри сценария
storage = StateMemoryStorage()

# Создаем сам объект бота
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
