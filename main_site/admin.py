from django.contrib import admin
from .models import Storage, Box, Subscription


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
