from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель 'Пользователи'. Поля first_name (Имя) и last_name (Фамилия) 
    обязательны к заполнению.
    """
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
