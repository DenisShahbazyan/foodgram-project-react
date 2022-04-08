from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    ADMIN = 'admin'


CHOICES_ROLE = (
    (UserRole.USER, 'user'),
    (UserRole.ADMIN, 'admin'),
)


class User(AbstractUser):
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
    role = models.CharField(
        verbose_name='Роль',
        max_length=16,
        choices=CHOICES_ROLE,
        default='user'
    )

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
