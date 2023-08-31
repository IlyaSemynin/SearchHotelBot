from loguru import logger
from keyboards.reply.buttons import count_hotel_button
from loader import bot
from states.user_data import (
    UserInfoState,
    DateRangeState,
    LowPriceInfoState,
    HighPriceInfoState,
)
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta


def get_calendar(is_process=False, callback_data=None, **kwargs):
    if is_process:
        result, key, step = DetailedTelegramCalendar(
            calendar_id=kwargs["calendar_id"],
            current_date=kwargs.get("current_date"),
            min_date=kwargs["min_date"],
            max_date=kwargs["max_date"],
            locale=kwargs["locale"],
        ).process(callback_data.data)
        return result, key, step
    else:
        calendar, step = DetailedTelegramCalendar(
            calendar_id=kwargs["calendar_id"],
            current_date=kwargs.get("current_date"),
            min_date=kwargs["min_date"],
            max_date=kwargs["max_date"],
            locale=kwargs["locale"],
        ).build()
        return calendar, step


ALL_STEPS = {"y": "год", "m": "месяц", "d": "день"}


def calendar_command(message: Message) -> None:
    today = date.today()
    calendar, step = get_calendar(
        calendar_id=1,
        current_date=today,
        min_date=today,
        max_date=today + timedelta(days=365),
        locale="ru",
    )

    bot.set_state(message.from_user.id, DateRangeState.check_in, message.chat.id)
    bot.send_message(
        message.from_user.id, f"Выберите {ALL_STEPS[step]}", reply_markup=calendar
    )


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def handle_arrival_date(call: CallbackQuery):
    today = date.today()
    result, key, step = get_calendar(
        calendar_id=1,
        current_date=today,
        min_date=today,
        max_date=today + timedelta(days=365),
        locale="ru",
        is_process=True,
        callback_data=call,
    )
    if not result and key:
        bot.edit_message_text(
            f"Выберите {ALL_STEPS[step]}",
            call.from_user.id,
            call.message.message_id,
            reply_markup=key,
        )
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["check_in"] = result  # Дата выбрана, сохраняем ее
            bot.edit_message_text(
                f"Дата заезда {result}", call.message.chat.id, call.message.message_id
            )
            logger.info(f"Выбрана дата заезда: {data['check_in']}")

            bot.send_message(call.from_user.id, "Выберите дату выезда")
            calendar, step = get_calendar(
                calendar_id=2,
                min_date=result + timedelta(days=1),
                max_date=result + timedelta(days=365),
                locale="ru",
            )
            bot.send_message(
                call.from_user.id, f"Выберите {ALL_STEPS[step]}", reply_markup=calendar
            )

            bot.set_state(
                call.from_user.id, DateRangeState.check_out, call.message.chat.id
            )


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_departure_date(call: CallbackQuery):
    today = date.today()
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        result, key, step = get_calendar(
            calendar_id=2,
            current_date=today,
            min_date=data["check_in"] + timedelta(days=1),
            max_date=data["check_in"] + timedelta(days=365),
            locale="ru",
            is_process=True,
            callback_data=call,
        )

    if not result and key:
        bot.edit_message_text(
            f"Выберите {ALL_STEPS[step]}",
            call.from_user.id,
            call.message.message_id,
            reply_markup=key,
        )

    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["check_out"] = result

            bot.edit_message_text(
                f"Дата выезда {result}", call.message.chat.id, call.message.message_id
            )
            logger.info(f"Выбрана дата выезда: {data['check_out']}")
            bot.send_message(
                call.from_user.id,
                "Выберите количество отелей",
                reply_markup=count_hotel_button(),
            )

            if data["command"] == "/low":
                bot.set_state(
                    call.from_user.id, LowPriceInfoState.count, call.message.chat.id
                )
            elif data["command"] == "/high":
                bot.set_state(
                    call.from_user.id, HighPriceInfoState.count, call.message.chat.id
                )
            else:
                bot.set_state(
                    call.from_user.id, UserInfoState.count, call.message.chat.id
                )
