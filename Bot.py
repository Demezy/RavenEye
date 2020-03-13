import datetime, sqlite3

from data.CONFIG import TG_API_URL, TG_TOKEN
from telegram import Bot, Update, ParseMode, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler, CallbackContext, ConversationHandler

from os.path import abspath

BUTTON1 = "Перейти на сайт 🌐"
BUTTON2 = "Приостановить ⏸"
BUTTON3 = "Настройки ⚙️"
BUTTON4 = "Задержка ⌛"
BUTTON5 = "Сброс 🔁"
BUTTON6 = "Назад ⬅️"
BUTTON7 = "Мой статус 🔐"

CALLBACK_BUTTON_SOS = "callback_button_sos"

conn_path = f'/{abspath("./data/userbase.db")}'


def mini_user_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1),
            KeyboardButton(BUTTON7),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def start_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1),
            KeyboardButton(BUTTON7),
        ],
        [
            KeyboardButton(BUTTON3),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def settings_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON2),
        ],
        [
            KeyboardButton(BUTTON4),
            KeyboardButton(BUTTON5),
        ],
        [
            KeyboardButton(BUTTON6),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def do_start(bot: Bot, update: Update):
    is_exists = check_id(update.message.chat_id)
    if not is_exists:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Привет! Напиши мне свой логин и код",
        )
    elif is_exists:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Вы успешно вышли из системы",
            reply_markup=ReplyKeyboardRemove(),
        )

        conn = sqlite3.connect(conn_path)
        cur = conn.cursor()
        sql = f"UPDATE user SET chat_id_telegram = 'Null' WHERE chat_id_telegram = '{update.message.chat_id}'"
        cur.execute(sql)
        conn.commit()
        conn.close()


def check_id(chat_id):
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    query = f"SELECT * FROM user WHERE chat_id_telegram='{chat_id}'"
    person = bool(cur.execute(query).fetchall())
    conn.close()
    return person


def check_user_type(chat_id):
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    query = f"SELECT user_type FROM user WHERE chat_id_telegram='{chat_id}'"
    user_type = cur.execute(query).fetchone()
    conn.close()
    return user_type[0]


def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Перейти на сайт 🌐\n(Выводится ссылка на сайт)\n\n"
             "Мой статус 🔐\n(Пользователь может узнать, какой у него статус (урезанный, обычный или админ))\n\n"
             "Остальные параметры доступны только для админа:\n"
             "Приостановить ⏸\n(Приостанавливает отправку сообщений на n количество секунд)\n\n"
             "Настройки ⚙\n(Открывает клавиатуру с расширенными настройками)\n\n"
             "Задержка ⌛\n(Указываестя время между отправкой сообщений в fps)\n\n"
             "Сброс 🔁\n(Сброс до заводских настроек)\n\n"
             "Назад ⬅️\n(Возвращает к основной клавиатуре)",
    )


def do_echo(bot: Bot, update: Update):
    is_exists = check_id(update.message.chat_id)
    if not is_exists:
        text = update.message.text
        conn = sqlite3.connect(conn_path)
        cur = conn.cursor()
        query = f"SELECT * FROM user WHERE username='{text.split()[0]}' AND telegram_key='{text.split()[1]}'"
        user_is_exist = bool(cur.execute(query).fetchall())
        conn.close()
        if user_is_exist:
            updater_id(update.message.chat_id, text.split()[0], text.split()[1]),
            user_type = check_user_type(update.message.chat_id)
            if user_type == 1:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Вы успешно авторизовались в системе!",
                    reply_markup=start_keyboard(),
                ),
            elif user_type == 2:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Вы успешно авторизовались в системе!",
                    reply_markup=mini_user_keyboard(),
                ),
            is_exists = True
        if not is_exists:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="😢неверно введены данные😭 ",
            )
    elif is_exists:
        text = update.message.text
        user_type = check_user_type(update.message.chat_id)
        if text == BUTTON1:
            update.message.reply_text(
                text="http://127.0.0.1:5000",
            )
        elif text == BUTTON2 and user_type == 1:
            update.message.reply_text(
                text="Пока что нет!",
            )
        elif text == BUTTON3 and user_type == 1:
            update.message.reply_text(
                text="С более подробным описание настроек Вы можете ознакомиться с помощью команды /help",
                reply_markup=settings_keyboard(),
            )
        elif text == BUTTON4 and user_type == 1:
            pass
        elif text == BUTTON5 and user_type == 1:
            pass
        elif text == BUTTON6 and user_type == 1:
            update.message.reply_text(
                text="Главная клавиатура",
                reply_markup=start_keyboard(),
            )
        elif text == BUTTON7:
            if user_type == 1:
                status = 'admin'
            elif user_type == 2:
                status = 'user'
            bot.send_message(
                chat_id=update.message.chat_id,
                text=f"Ваш статус: {status} \n",
            )
        elif user_type == 1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Клавиатура открыта!",
                reply_markup=start_keyboard(),
            )
        elif user_type == 2:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Клавиатура открыта!",
                reply_markup=mini_user_keyboard(),
            )


def send_image(path):
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    query = f"SELECT chat_id_telegram FROM user"
    all_users_id = cur.execute(query).fetchall()
    conn.close()
    for user_id in all_users_id:
        for id in user_id:
            try:
                bot.send_photo(
                    chat_id=id,
                    photo=open(path, 'rb'),
                )
            except Exception as e:
                print(e)


def updater_id(chat_id, login_data, code_data):
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    sql = f"UPDATE user SET chat_id_telegram = '{chat_id}' WHERE username = '{login_data}' AND telegram_key = '{code_data}'"
    cur.execute(sql)
    conn.commit()
    conn.close()


def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    reg_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(reg_handler)

    # Начать обработку входящих сообщений
    updater.start_polling()
    # Не прерывать скрипт до обработки всех сообщений
    updater.idle()


if __name__ == '__main__':
    main()
