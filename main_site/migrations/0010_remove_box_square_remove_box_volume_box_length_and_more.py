# Generated by Django 4.2 on 2023-04-19 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0009_remove_box_length_remove_box_width_box_square_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='square',
        ),
        migrations.RemoveField(
            model_name='box',
            name='volume',
        ),
        migrations.AddField(
            model_name='box',
            name='length',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Длина бокса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='box',
            name='width',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Ширина бокса'),
            preserve_default=False,
        ),
    ]
