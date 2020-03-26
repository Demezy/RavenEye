from os.path import abspath
from os import makedirs
from os.path import exists

import sqlite3
import telebot

from data.CONFIG import TG_TOKEN

cam = None
link = '127.0.0.1:5000'
bot = telebot.TeleBot(TG_TOKEN)
conn_path = f'/{abspath("./data/userbase.db")}'

SiteButton = "Перейти на сайт 🌐"
PathButton = "Путь 📂"
SettingsButton = "Настройки ⚙️"
MinAreaButton = "Минимальная область 🔬"
MaxAreaButton = "Максимальная область 🔭"
BackButton = "Назад ⬅️"
StatusButton = "Мой статус 🔐"
LogoutButton = "Выйти из системы 🚪"
SizeButton = "Размер изображения 🖼"

min_user_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
min_user_keyboard.row(SiteButton, StatusButton)
min_user_keyboard.row(LogoutButton)

user_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboard.row(SiteButton, StatusButton)
user_keyboard.row(LogoutButton)
user_keyboard.row(SettingsButton)

settings_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
settings_keyboard.row(PathButton)
settings_keyboard.row(MinAreaButton, MaxAreaButton)
settings_keyboard.row(SizeButton)
settings_keyboard.row(BackButton)


# start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Напиши /login, чтобы войти в систему!')


# bot
@bot.message_handler(commands=['help'])
def do_help(message):
    bot.send_message(message.chat.id,
                     "Перейти на сайт 🌐\n(Выводится ссылка на сайт)\n\n"
                     "Мой статус 🔐\n(Пользователь может узнать свой логин и статус (обычный или админ))\n\n"
                     "Выйти из системы 🚪\n(Пользователь может выйти из системы, чтобы зайти под другой учётной "
                     "записью)\n\n"
                     "Настройки ⚙\n(Открывает клавиатуру с расширенными настройками, доступную только для "
                     "администраторов)\n\n"
                     "Назад ⬅️\n(Возвращает к основной клавиатуре)"
                     "Путь 📂\n(Пользователь может выбрать удобную для себя дирикторию, в которую будут сохраняться "
                     "кадры)\n\n"
                     "Минимальная область 🔬\n(Та площадь объекта, которой будет пренебрегать система)\n\n"
                     "Максимальная область 🔭\n(Параметр ответственный за адаптацию к изменению освещённости )\n\n",
                     )


def check_id_and_user_type(chat_id):
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    query = f"SELECT username, user_type FROM user WHERE chat_id_telegram='{chat_id}'"
    name_and_type = cur.execute(query).fetchone()
    conn.close()
    return name_and_type


# echo function
@bot.message_handler(content_types=['text'])
def send_text(message):
    is_exists = check_id_and_user_type(message.chat.id)
    if bool(is_exists):
        if message.text == SiteButton:
            bot.send_message(message.chat.id, f'Нажмите {link}, чтобы перейти на сайт')
        elif message.text == StatusButton:
            if is_exists[1] == 1:
                u_type = 'admin'
            else:
                u_type = 'user'
            bot.send_message(message.chat.id, f'{is_exists[0]}, Ваш статус: {u_type}')
        elif message.text == PathButton and is_exists[1] == 1:
            bot.send_message(message.chat.id, "Введите путь до необходимой дириктории")
            bot.register_next_step_handler(message, change_save_path)
        elif message.text == BackButton and is_exists[1] == 1:
            bot.send_message(message.chat.id, "Главная клавиатура", reply_markup=user_keyboard)
        elif message.text == SizeButton and is_exists[1] == 1:
            bot.send_message(message.chat.id, "Введите желаемый размер кадра 'ширина' 'высота' в пикселях")
            bot.register_next_step_handler(message, change_image_size)
        elif message.text == MinAreaButton:
            bot.send_message(message.chat.id, "Отсев изменений меньших заданной площади в пикселях")
            bot.register_next_step_handler(message, change_min_area)
        elif message.text == MaxAreaButton:
            bot.send_message(message.chat.id, "Введите площадь в пикселях (не советуется изменять)")
            bot.register_next_step_handler(message, change_max_area)
        elif message.text == LogoutButton:
            bot.send_message(message.chat.id, "Вы успешно вышли из системы",
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            conn = sqlite3.connect(conn_path)
            cur = conn.cursor()
            sql = f"UPDATE user SET chat_id_telegram = Null WHERE chat_id_telegram = '{message.chat.id}'"
            cur.execute(sql)
            conn.commit()
            conn.close()
        elif message.text == SettingsButton and is_exists[1] == 1:
            bot.send_message(message.chat.id, 'Клавиатура откыта!', reply_markup=settings_keyboard)
        elif is_exists[1] == 1:
            bot.send_message(message.chat.id, 'Клавиатура откыта!', reply_markup=user_keyboard)
        elif is_exists[1] == 2:
            bot.send_message(message.chat.id, 'Клавиатура откыта!', reply_markup=min_user_keyboard)
    elif not bool(is_exists):
        if message.text == '/login':
            bot.send_message(message.chat.id, "Введи свои данные (логин и ключ)"),
            bot.register_next_step_handler(message, registration)  # следующий шаг – функция get_name
        else:
            bot.send_message(message.chat.id, 'Напиши /login, чтобы войти в систему!')


def change_save_path(message):
    path = message.text
    try:
        if not exists(path):
            makedirs(path)
        cam.change_parameters(path=path)
        bot.send_message(message.chat.id, f"Путь изменён на '{path}'")
    except Exception as e:
        # print(e)
        bot.send_message(message.chat.id, "Не удалось изменить дирикторию!\nПопробуйте ещё раз...")


def change_image_size(message):
    size = message.text
    try:
        width = size.split()[0]
        height = size.split()[1]
        width = int(width)
        height = int(height)
        cam.change_parameters(width=width, height=height)
    except Exception as e:
        # print(e)
        bot.send_message(message.chat.id, "Не удалось изменить размер кадра!\nПопробуйте ещё раз...")


def change_min_area(message):
    min_area = message.text
    try:
        min_area = int(min_area)
        cam.change_parameters(min_area=min_area)
    except Exception as e:
        # print(e)
        bot.send_message(message.chat.id, "Не удалось изменить минимальную площадь!\nПопробуйте ещё раз...")


def change_max_area(message):
    max_area = message.text
    try:
        max_area = int(max_area)
        cam.change_parameters(max_area=max_area)
    except Exception as e:
        # print(e)
        bot.send_message(message.chat.id, "Не удалось изменить максимальную площадь!\nПопробуйте ещё раз...")


def send_image(path):
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    query = f"SELECT chat_id_telegram FROM user"
    all_users_id = cur.execute(query).fetchall()
    conn.close()
    for user_id in all_users_id:
        for ID in user_id:
            try:
                bot.send_photo(ID, open(abspath(path), 'rb'))
            except TypeError:
                pass
            except Exception as e:
                print(e)


def registration(message):  # получаем фамилию
    user_data = message.text
    try:
        user_name = user_data.split()[0]
        user_key = user_data.split()[1]
        conn = sqlite3.connect(conn_path)
        cur = conn.cursor()
        query = f"SELECT user_type FROM user WHERE username='{user_name}' AND telegram_key='{user_key}'"
        user_type = cur.execute(query).fetchone()
        user_is_exist = bool(user_type)
        conn.close()
        if user_is_exist:
            if user_type[0] == 1:
                updater_id(message.chat.id, user_name, user_key)
                bot.send_message(message.chat.id, 'Вы успешно авторизовались в системе!', reply_markup=user_keyboard)
            elif user_type[0] == 2:
                updater_id(message.chat.id, user_name, user_key)
                bot.send_message(message.chat.id, 'Вы успешно авторизовались в системе!',
                                 reply_markup=min_user_keyboard)
            elif user_type[0] == 3:
                bot.send_message(message.chat.id, 'Недостаточно прав!')
        else:
            bot.send_message(message.chat.id, 'Данные введены неверно!\nПопробуйте ещё раз...')
            bot.register_next_step_handler(message, registration)
    except Exception:
        bot.send_message(message.chat.id, 'Вы забыли ввести логин или ключ!\nПопробуйте ещё раз...')


def updater_id(chat_id, login_data, code_data):
    conn = sqlite3.connect(conn_path)
    cur = conn.cursor()
    sql = f"UPDATE user SET chat_id_telegram = '{chat_id}' WHERE username = '{login_data}' " \
          f"AND telegram_key = '{code_data}'"
    cur.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    from CamDetect import Detector

    cam = Detector()
    bot.polling()
