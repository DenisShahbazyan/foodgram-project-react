from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель 'Пользователи'. Поля first_name (Имя) и last_name (Фамилия)
    обязательны к заполнению.
    """
    username = models.CharField(
        verbose_name='имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150
    )
    subscribe = models.ManyToManyField(
        'self',
        verbose_name='подписка',
        related_name='subscribers',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['id']
