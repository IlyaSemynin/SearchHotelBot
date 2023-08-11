from loader import bot  # импорт бота из файла loader.py
import handlers  # noqa импорт папки обработчиков сообщений (хэндлеров)
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands  # импорт команд которые будут вызываться из кнопки "Меню"

if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)  # установка в кнопку "Меню" команд
    bot.infinity_polling()  # бесконечный запуск бота
