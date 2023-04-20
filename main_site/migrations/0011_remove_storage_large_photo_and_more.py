# Generated by Django 4.2 on 2023-04-20 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0010_remove_box_square_remove_box_volume_box_length_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storage',
            name='large_photo',
        ),
        migrations.RemoveField(
            model_name='storage',
            name='small_photo',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Фото склада')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main_site.storage', verbose_name='Хранилище')),
            ],
            options={
                'verbose_name': 'Фотография склада',
                'verbose_name_plural': 'Фотографии склада',
            },
        ),
    ]