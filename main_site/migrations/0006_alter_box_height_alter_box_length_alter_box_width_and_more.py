# Generated by Django 4.2 on 2023-04-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0005_storage_rental_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='height',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Высота бокса'),
        ),
        migrations.AlterField(
            model_name='box',
            name='length',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Длина бокса'),
        ),
        migrations.AlterField(
            model_name='box',
            name='width',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Ширина бокса'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='rental_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Цена аренды'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Температура на складе'),
        ),
    ]
