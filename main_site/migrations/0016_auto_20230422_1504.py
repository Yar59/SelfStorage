# Generated by Django 4.2 on 2023-04-22 12:04
import os

from django.core.files.base import ContentFile
from django.db import migrations
from self_storage.settings import BASE_DIR as base_dir


def create_images(apps, schema_editor):
    Storage = apps.get_model('main_site', 'Storage')
    Image = apps.get_model('main_site', 'Image')
    storages = Storage.objects.all()
    for storage in storages:
        for image_index in range(2):
            with open('static/img/image2.png', 'rb') as file:
                content = file.read()
                Image.objects.get_or_create(
                    storage=storage,
                    image=ContentFile(content, name='image2.png')
                )


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0015_auto_20230422_1351'),
    ]

    operations = [
        migrations.RunPython(create_images)
    ]

