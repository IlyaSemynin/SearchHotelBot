import os
from loader import bot
from states.user_data import UserInfoState
from telebot.types import Message
from keyboards.reply.buttons import delete_history
from database.history_class import History


@bot.message_handler(commands=["history"])
def view_history(message: Message) -> None:
    """
    Обработчик команды history. Выводит в чат историю поиска полученную из БД.
    :param message: Message
    :return: None
    """
    history_dict = History("bot_history.sqlite", str(message.from_user.id))
    count = history_dict.count
    bot.set_state(message.from_user.id, UserInfoState.clean_history, message.chat.id)
    print(count)
    err_cnt = 0
    for key in range(0, 100):
        try:
            if err_cnt >= 99:
                bot.send_message(message.from_user.id, "Ничего не найдено")
                bot.delete_state(message.from_user.id)
                break
            text = (
                f"ID Пользователя: {history_dict.get_user_id(key)}\n"
                f"Команда: {history_dict.get_command(key)}\n"
                f"Время обращения: {history_dict.get_date(key)}\n"
                f"Номер обращения: {key}\n"
                f"{''.join(history_dict.get_hotels(key))}"
            )
            bot.send_message(message.from_user.id, text, reply_markup=delete_history())
            err_cnt -= 1
        except:
            err_cnt += 1
            continue
    history_dict.close()


@bot.message_handler(state=UserInfoState.clean_history)
def clean_history(message: Message) -> None:
    """
    Функция для очистки истории сообщений.
    :param message:
    :return:
    """
    try:
        bot.delete_state(message.from_user.id)
        os.unlink("bot_history.sqlite")
        bot.send_message(message.from_user.id, "История очищена")
    except:
        bot.send_message(message.from_user.id, "История пуста")
        bot.delete_state(message.from_user.id)