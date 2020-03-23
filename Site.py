import random
from flask import Flask, flash, Response, render_template, redirect, url_for, request, abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, IntegerField, validators
from wtforms.validators import InputRequired, Email, Length
from time import sleep

from os.path import abspath

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{abspath("./data/userbase.db")}'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

COUNT_USER_TYPE = 3
Camera = None
fps = 20


def key_gen():
    key = ''

    for i in range(16):
        if i % 4 == 0 and i != 0:
            key += '-'
        key += chr(random.randint(ord('A'), ord("Z")))

    return key


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    telegram_key = db.Column(db.String(80), default=key_gen)
    chat_id_telegram = db.Column(db.String(80))
    user_type = db.Column(db.Integer, nullable=False)


class MyModelView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        if current_user.user_type == 1 and current_user.is_authenticated:
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

    excluded_list_columns = ('password',)  # Не выводятся в таблицу юзеров
    form_rules = ['username', 'email', 'password', 'telegram_key', 'chat_id_telegram',
                  'user_type']  # Параметры для редактирования
    column_searchable_list = ['username', 'email', 'telegram_key', 'chat_id_telegram',
                              'user_type']  # Столбцы работающие с поиском


admin = Admin(app, name='🅐🅓🅜🅘🅝 🅟🅐🅝🅔🅛',
              index_view=MyModelView(User, db.session, name='User Data', url='/panel/admin', endpoint='admin'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    email = StringField('email')
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    user_type = IntegerField('user_type',
                             validators=[InputRequired(), validators.NumberRange(min=1, max=COUNT_USER_TYPE)])


@app.route('/home')
@login_required
def index():
    return render_template('index.html')


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('base'))
        return render_template('login.html', form=form, error_message='Invalid username or password')

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                            telegram_key=key_gen, user_type=form.user_type.data)
            db.session.add(new_user)
            db.session.commit()
        else:
            return render_template('signup.html', form=form, error_message='This nickname is already taken')

        return render_template('login.html', form=form)

    return render_template('signup.html', form=form)


@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html', name=current_user.username, email=current_user.email,
                           telegram_key=current_user.telegram_key, user_type=current_user.user_type)


@app.route('/changer_information', methods=['GET', 'POST'])  # Correct personal user information
@login_required
def chang_information():
    error_mess = ''
    cool_news = ''
    user_data = User.query.filter_by(username=current_user.username).first()
    if check_password_hash(user_data.password, request.form['curr_pass']):

        if request.form['new_pass'] != '':
            if request.form['confirm_pass'] != '':
                if request.form['new_pass'] == request.form['confirm_pass']:
                    if check_password_hash(user_data.password, request.form['confirm_pass']) is False:
                        user_data.password = generate_password_hash(request.form['confirm_pass'], method='sha3-256')
                        db.session.commit()
                        cool_news = 'Данные успешно изменены'
                    else:
                        error_mess = 'Вы не можете указать свой текущий пароль'
                else:
                    error_mess = 'Повторный пароль введён неверно'
            else:
                error_mess = 'Введите пароль повторно'
        else:
            pass

        if request.form['email'] != current_user.email:
            user_data.email = request.form['email']  # Change email
            db.session.commit()
            cool_news = 'Данные успешно изменены'
        else:
            pass

        if request.form['nickname'] != current_user.username:
            user = User.query.filter_by(username=request.form['nickname']).first()
            if user is None:
                change_user = User.query.filter_by(username=current_user.username).first()
                change_user.username = request.form['nickname']  # Change username
                db.session.commit()
                cool_news = 'Данные успешно изменены'
            else:
                error_mess = 'Такой юзер уже есть'
        else:
            pass
    else:
        error_mess = "Неверно введён пароль"
    return render_template('panel.html', name=current_user.username, email=current_user.email,
                           telegram_key=current_user.telegram_key, error_message=error_mess, cool_mess=cool_news,
                           user_type=current_user.uset_type)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def gen(camera):
    """Video streaming generator function."""
    while True:
        sleep(1 / fps)
        frame = camera.get_frame_obj()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


app.run()