from django.db import models
import random
from django.contrib.auth.forms import AuthenticationForm


def key_gen():
    key = ''

    for i in range(16):
        if i % 4 == 0 and i != 0:
            key += '-'
        key += chr(random.randint(ord('A'), ord("Z")))

    return key


class User(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    username = models.CharField('username', max_length=20, unique=True)
    email = models.CharField('email', max_length=50)
    password = models.TextField('password')
    telegram_key = models.TextField('telegram_key', max_length=80, default=key_gen)
    chat_id_telegram = models.CharField('chat_id_telegram', max_length=10)
    user_type = models.IntegerField('user_type', null=False)

    def __str__(self):
        return 'Name - {0}, Email - {1}, Password - {2}, TelegramKey - {3}, ChatIdTelegram - {4}, UserType - {5}'.format(
            self.username,
            self.email,
            self.password,
            self.telegram_key,
            self.chat_id_telegram,
            self.user_type)
