from loader import bot  # импорт бота из файла loader.py
import handlers  # noqa импорт папки обработчиков сообщений (хэндлеров)
from utils.set_bot_commands import set_default_commands  # импорт команд которые будут вызываться из кнопки "Меню"

if __name__ == "__main__":
    set_default_commands(bot)  # установка в кнопку "Меню" команд
    bot.infinity_polling()  # бесконечный запуск бота
