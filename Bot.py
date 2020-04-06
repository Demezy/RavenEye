from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select, update, and_, or_
from os.path import abspath, exists
from os import makedirs

import telebot, requests

from data.CONFIG import TG_TOKEN, Link

link = 'https://' + Link + ':8000'
cam = None
bot = telebot.TeleBot(TG_TOKEN)
engine = create_engine(f'sqlite:///{abspath("./data/userbase.db")}')
meta = MetaData()

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


user = Table(
    'user', meta, 
    Column('id', Integer, primary_key=True),
    Column('username', String(15), unique=True), 
    Column('email', String(50)),
    Column('password', String(80)),
    Column('telegram_key', String(80)),
    Column('chat_id_telegram', String(80)),
    Column('user_type', Integer, nullable=False), 
)


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
    conn = engine.connect()
    stmt = select([user.c.username, user.c.user_type]).where(user.c.chat_id_telegram==f'{chat_id}')
    name_and_type = conn.execute(stmt).fetchone()
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
            conn = engine.connect()
            stmt = update(user).where(user.c.chat_id_telegram==f'{message.chat.id}').values(chat_id_telegram=None)
            conn.execute(stmt)
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
    conn = engine.connect()
    stmt = select([user.c.chat_id_telegram])
    all_users_id = conn.execute(stmt).fetchall()
    conn.close()
    for user_id in all_users_id:
        for ID in user_id:
            try:
                bot.send_photo(ID, open(abspath(path), 'rb'))
            except TypeError:
                pass
            except Exception as e:
                print(e)


def registration(message):  # авторизация в системе
    user_data = message.text
    try:
        user_name = user_data.split()[0]
        user_key = user_data.split()[1]
        conn = engine.connect()
        stmt = select([user.c.user_type]).where(and_(user.c.username==f'{user_name}', user.c.telegram_key==f'{user_key}'))
        user_type = conn.execute(stmt).fetchone()
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
    conn = engine.connect()
    sql = f"UPDATE user SET chat_id_telegram = '{chat_id}' WHERE username = '{login_data}' " \
          f"AND telegram_key = '{code_data}'"
    stmt = update(user).where(and_(user.c.username==f'{login_data}', user.c.telegram_key==f'{code_data}')).values(chat_id_telegram = f'{chat_id}')
    conn.execute(stmt)
    conn.close()
