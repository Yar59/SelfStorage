# Generated by Django 4.2 on 2023-04-19 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0007_storage_large_photo_storage_small_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='note',
            field=models.CharField(blank=True, max_length=35, null=True, verbose_name='Заметка'),
        ),
    ]