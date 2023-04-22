# Generated by Django 4.2 on 2023-04-21 17:18
import random

from django.db import migrations


def create_storages(apps, schema_editor):

    names = [
        'Средний склад', 'Хранилище', 'Промзона', 'Место хранения', 'Storage Mart',
        'Мини-хранилище Manhattan', 'Освободить место', 'Самостоятельное хранение Lone Star',
        'Дополнительное пространство для хранения', 'Мини-хранилище Cornerstone',
        'Климат-контроль хранения', 'Кладовая на чердаке', 'Центры хранения All Seasons'
    ]

    addresses = [
        'Саратовская область, город Видное, ул. Славы, 84',
        'Курская область, город Шатура, пр. Будапештсткая, 22',
        'Кемеровская область, город Москва, спуск Ладыгина, 95',
        'Читинская область, город Орехово-Зуево, наб. Ломоносова, 08',
        'Ростовская область, город Коломна, пл. 1905 года, 52',
        'Владимирская область, город Балашиха, въезд Ломоносова, 16',
        'Ярославская область, город Красногорск, наб. Ломоносова, 89',
    ]

    notes = [
        'Рядом с метро', 'Низкая цена', 'Большие боксы', 'Оптимальная температура на складе'
    ]

    Storage = apps.get_model('main_site', 'Storage')
    for address in addresses:
        Storage.objects.get_or_create(
            name=random.choice(names),
            address=address,
            temperature=("%.2f" % random.uniform(10.0, 25.0)),
            rental_price=random.randrange(100, 300, 50),
            note=random.choice(notes)
        )


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0012_alter_storage_address'),
    ]

    operations = [
        migrations.RunPython(create_storages)
    ]