# Generated by Django 4.2 on 2023-04-19 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0008_storage_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='length',
        ),
        migrations.RemoveField(
            model_name='box',
            name='width',
        ),
        migrations.AddField(
            model_name='box',
            name='square',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Площадь бокса'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='box',
            name='volume',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='Объем бокса'),
            preserve_default=False,
        ),
    ]
