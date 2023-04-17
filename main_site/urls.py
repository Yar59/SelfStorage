from django.urls import path

from .views import *

app_name = 'main_site'

urlpatterns = [
    path('', show_main_page, name='index'),
]