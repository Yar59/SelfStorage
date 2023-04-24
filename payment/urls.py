from django.urls import path

from .views import *

app_name = 'payment'

urlpatterns = [
    path('success/', pay_success, name='successed_payment'),
    path('canselled/', cancelled, name='cancelled_payment'),
    path('<int:box_pk>', make_payment, name='make_payment'),
]
