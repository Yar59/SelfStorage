from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Missing email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, is_staff=True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя', max_length=250, default='some_user')
    email = models.EmailField('Адрес электронной почты', max_length=50, unique=True)
    is_staff = models.BooleanField('Является ли менеджером?', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Storage(models.Model):
    name = models.CharField('Название', max_length=20)
    address = models.CharField('Адрес', max_length=30)

    class Meta:
        verbose_name = "Хранилище"
        verbose_name_plural = "Хранилища"

    def __str__(self):
        return f'{self.name} - {self.address}'


class Box(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Хранилище',
        on_delete=models.CASCADE,
        related_name='boxes'
    )
    number = models.CharField(
        'Номер бокса',
        max_length=20,
        unique=True
    )
    width = models.DecimalField('Ширина бокса', decimal_places=5, max_digits=10)
    length = models.DecimalField('Длина бокса', decimal_places=5, max_digits=10)
    height = models.DecimalField('Высота бокса', decimal_places=5, max_digits=10)
    floor = models.PositiveIntegerField('Этаж')

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

    def __str__(self):
        return f'{self.storage} - №{self.number}'


class Subscription(models.Model):
    start_date = models.DateField('Начало аренды')
    end_date = models.DateField('Конец аренды')
    type = models.CharField('Тип подписки', max_length=10)

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    box = models.ForeignKey(
        Box,
        verbose_name='Бокс',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'{self.user.name} - №{self.box.number} до {self.end_date}'
