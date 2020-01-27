import datetime, mysql.connector

from config import TG_API_URL, TG_TOKEN
from telegram import Bot, Update, ParseMode, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackQueryHandler, CallbackContext, ConversationHandler


BUTTON1 = "SMS ✉️"
BUTTON2 = "Super ⚡️"
BUTTON3 = "Время ⏰"
CALLBACK_BUTTON_SOS = "callback_button_sos"

TITLES = {
    CALLBACK_BUTTON_SOS: "ДА\nТОЧНО 🆘",
}


def get_keyboard3():
    keyboard = [
        [
            KeyboardButton(BUTTON1),
            KeyboardButton(BUTTON2),
        ],
        [
            KeyboardButton(BUTTON3),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def sos_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON_SOS], callback_data=CALLBACK_BUTTON_SOS),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(bot: Bot, update: Update):
    query = update.callback_query
    data = query.data

    if data == CALLBACK_BUTTON_SOS:
        query.edit_message_text(
            text="Ты что дурак, зачем ты это делаешь?\n"
                 "Во-первых: ты сделал ложный вызов\n"
                 "Во-вторых: если тебя действительно грабят,\n"
                 "То мне тебя действительно жаль,\n"
                 "Ведь эта кнопка ещё не работает\n"
                 "Вместо того, чтобы фигнёй заниматься с БОТОМ,\n"
                 "Лучшебы бежал звонить в полицию =)",
        )


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Напиши мне свой логин и код",
    )

    # проверка с выводом


def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Это учебный бот\n\n"
             "Список доступных команд есть в меню\n\n"
             "Можешь даже не смотреть, их там всего две: /start и /help\n"
             "впрочем, ничего интересного",
    )


def check_id(chat_id):
    conn = mysql.connector.connect(
        user='mysql',
        password='mysql',
        host='127.0.0.1',
        database='my2')
    global acc_connect
    cur = conn.cursor()
    query = "SELECT chat_id_telegram FROM users"
    cur.execute(query)
    conn.close()
    for chat_id_telegram in cur:
        if chat_id_telegram[0] == chat_id:
            acc_connect = 'True'
            break
        else:
            acc_connect = 'False'


def do_echo(bot: Bot, update: Update):
    check_id(update.message.chat_id)
    global acc_connect
    if acc_connect == 'False':
        conn = mysql.connector.connect(
            user='mysql',
            password='mysql',
            host='127.0.0.1',
            database='my2')
        cur = conn.cursor()
        query = "SELECT * FROM users"
        cur.execute(query)
        conn.close()
        text = update.message.text  # '101 DCE93-50B4F-0DDE1-CEDB6-8B05D'
        for (id, login, email, password, code, chat_id_telegram) in cur:
            # print("{}, {}, {}, {}, {}".format(id, login, email, code, chat_id_telegram))
            if str(login) == text.split()[0]:  # '101'
                if str(code) == text.split()[1]:  # 'DCE93-50B4F-0DDE1-CEDB6-8B05D'
                    updater_id(update.message.chat_id, text.split()[0], text.split()[1]),
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Вы успешно авторизовались в системе!",
                        reply_markup=get_keyboard3(),
                    ),
                    acc_connect = 'True'
        if acc_connect == 'False':
            bot.send_message(
                chat_id=update.message.chat_id,
                text="😢неверно введены данные😭 ",
            )
    elif acc_connect == 'True':
        text = update.message.text
        if text == BUTTON1:
            update.message.reply_text(
                text="Эта кнопка посылает сообщение\nо нарушении охранной компании,\nВы точно хотите этого?",
                reply_markup=sos_keyboard(),
            )
        elif text == BUTTON2:
            update.message.reply_text(
                text="Ах, да, как же я забыл предупредить, что эта кнопка не работает,\n"
                     "как-нибудь потом напишу к ним функционал",
            )
        elif text == BUTTON3:
            now = datetime.datetime.now()
            text = "Точное время 👇\n" \
                   "-----------------------\n" \
                   "\n{}".format(now)
            update.message.reply_text(
                text=text,
            )
        elif text.lower() == "открыть клавиатуру":
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Клавиатура открыта!",
                reply_markup=get_keyboard3(),
            )


def send_image(path):
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    bot.send_photo(
        chat_id=510560017,
        photo=open('maxresdefault.jpg', 'rb'),
    )


def updater_id(chat_id, login_data, code_data):
    conn = mysql.connector.connect(
        user='mysql',
        password='mysql',
        host='127.0.0.1',
        database='my2')
    cur = conn.cursor()
    sql = "UPDATE users SET chat_id_telegram = '{}' WHERE login = '{}' AND code = '{}'".format(chat_id, login_data, code_data)
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
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
    reg_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(reg_handler)
    updater.dispatcher.add_handler(buttons_handler)

    # Начать обработку входящих сообщений
    updater.start_polling()
    # Не прерывать скрипт до обработки всех сообщений
    updater.idle()


if __name__ == '__main__':
    main()
