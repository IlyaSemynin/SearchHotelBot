from telebot.types import Message
from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Стандартная команда echo которая срабатывает если что-то пошло не по плану и бот не понимает пользователя.
    :param message: Message
    :return: None
    """
    bot.reply_to(
        message,
        f"Привет, {message.from_user.full_name}!"
        f"\nЧтобы начать, выбери команду воспользовавшись кнопкой 'Меню'",
    )
