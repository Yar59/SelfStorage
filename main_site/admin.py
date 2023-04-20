from django.contrib import admin
from django.utils.html import format_html

from .models import Storage, Box, Subscription, Image


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ['place_images']
    extra = 0
    def place_images(self, image_object):

        return format_html('<img src="{}" height=200px />', image_object.image.url)

    place_images.short_description = 'Миниатюра'


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

