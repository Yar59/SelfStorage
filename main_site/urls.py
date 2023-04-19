from django.urls import path
from django.contrib import admin
from .views import *

app_name = 'main_site'

urlpatterns = [
    path('', show_main_page, name='main'),
    path('boxes/', show_boxes, name='boxes'),
    path('my_rent/', show_my_rent, name='my_rent'),
    path('faq/', show_faq, name='faq'),
]