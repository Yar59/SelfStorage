from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Count
from phonenumber_field.modelfields import PhoneNumberField


class BoxQuerySet(models.QuerySet):
    def free(self):
        return self.annotate(subscriptions_count=Count('subscriptions')).filter(subscriptions_count=0)


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
    phonenumber = PhoneNumberField('Номер телефона', blank=True, null=True)
    is_staff = models.BooleanField('Является ли менеджером?', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Storage(models.Model):
    name = models.CharField('Название', max_length=50)
    address = models.CharField('Адрес', max_length=100)
    temperature = models.DecimalField('Температура на складе', decimal_places=2, max_digits=5)
    rental_price = models.DecimalField('Цена аренды', decimal_places=2, max_digits=8)
    note = models.CharField(null=True, blank=True, max_length=35, verbose_name='Заметка')

    class Meta:
        verbose_name = 'Хранилище'
        verbose_name_plural = 'Хранилища'

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
    width = models.DecimalField('Ширина бокса', decimal_places=2, max_digits=5)
    length = models.DecimalField('Длина бокса', decimal_places=2, max_digits=5)
    height = models.DecimalField('Высота бокса', decimal_places=2, max_digits=5)
    floor = models.PositiveIntegerField('Этаж')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'{self.storage} - №{self.number}'

    objects = BoxQuerySet.as_manager()


class Image(models.Model):
    storage = models.ForeignKey(
        Storage,
        verbose_name='Хранилище',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(blank=True, verbose_name='Фото склада')

    class Meta:
        verbose_name = 'Фотография склада'
        verbose_name_plural = 'Фотографии склада'

    def __str__(self):
        return f'{self.storage.name} {self.id}'


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
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.username} - №{self.box.number} до {self.end_date}'


def action(query, value):
    return query.extra(where=['number + 1 = %s'], params=[value])

