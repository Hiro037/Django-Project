from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail")

    phone_number = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    pfp = models.ImageField(
        verbose_name="Аватар пользователя", upload_to="users_pfp", blank=True, null=True
    )

    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        help_text="Выберите свою страну",
        blank=True,
        null=True,
    )

    token = models.CharField(
        max_length=100, verbose_name="Токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
