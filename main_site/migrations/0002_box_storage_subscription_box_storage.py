# Generated by Django 4.2 on 2023-04-19 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, unique=True, verbose_name='Номер бокса')),
                ('width', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Ширина бокса')),
                ('length', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Длина бокса')),
                ('height', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Высота бокса')),
                ('floor', models.PositiveIntegerField(verbose_name='Этаж')),
            ],
            options={
                'verbose_name': 'Бокс',
                'verbose_name_plural': 'Боксы',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('address', models.CharField(max_length=30, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Хранилище',
                'verbose_name_plural': 'Хранилища',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Начало аренды')),
                ('end_date', models.DateField(verbose_name='Конец аренды')),
                ('type', models.CharField(max_length=10, verbose_name='Тип подписки')),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_site.box', verbose_name='Бокс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddField(
            model_name='box',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_site.storage', verbose_name='Хранилище'),
        ),
    ]
