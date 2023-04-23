import logging
from datetime import datetime, timedelta
from smtplib import SMTPDataError
from time import sleep

from django.core.management import BaseCommand
from django.conf import settings

from main_site.mailer import *
from main_site.models import *


class Command(BaseCommand):
    help = 'Запустите для рассылки сообщений на почту'

    def handle(self, *args, **kwargs):
        while True:
            last_day_payments, three_days_payments, five_day_payments = get_soon_payments()
            print(last_day_payments, three_days_payments, five_day_payments)
            for subscription in last_day_payments:
                create_rent_over_notification(subscription)
            last_day_payments.update(latest_notification=datetime.now())

            for subscription in three_days_payments:
                create_payment_notification(subscription)
            three_days_payments.update(latest_notification=datetime.now())

            for subscription in five_day_payments:
                create_payment_notification(subscription)
            five_day_payments.update(latest_notification=datetime.now())
            sleep(120)


def get_soon_payments():
    today = datetime.now()
    five_days_after = datetime.now() + timedelta(5)
    three_days_after = datetime.now() + timedelta(3)
    yesterday = datetime.now() - timedelta(1)

    last_day_payments = Subscription.objects\
        .filter(end_date__lte=today)\
        .exclude(latest_notification=today)
    three_days_payments = Subscription.objects\
        .filter(end_date__lte=three_days_after)\
        .exclude(end_date__lte=today)\
        .exclude(latest_notification__gte=yesterday)
    five_day_payments = Subscription.objects\
        .filter(end_date__lte=five_days_after)\
        .exclude(end_date__lte=today)\
        .exclude(end_date__lte=three_days_after)
    return last_day_payments, three_days_payments, five_day_payments


def create_payment_notification(subscription):
    try:
        box_number = subscription.box.number
        html_content = f'''
                    <h1>Аренда бокса №{box_number} истекает</h1>
                    <p>
                      Продлите аренду до {subscription.end_date} или заберите вещи
                      из хранилища до окончания срока аренды
                    </p>
                    '''

        send_email(
            f'Аренда бокса №{box_number} истекает',
            subscription.user.email,
            text_content=f'Привет,{subscription.user.username}',
            html_content=html_content,
        )
    except SMTPDataError:
        logging.exception('Ошибка при отправке сообщения')


def create_rent_over_notification(subscription):
    try:
        box_number = subscription.box.number
        disposal_date = (datetime.now() + timedelta(30)).date
        html_content = f'''
                <h1>Аренда бокса №{box_number} истекла</h1>
                <p>
                  Продлите аренду или заберите вещи до {subscription.end_date}, 
                  иначе они будут уничтожены после {disposal_date} 
                </p>
                '''

        send_email(
            f'Аренда бокса №{box_number} истекла',
            subscription.user.email,
            text_content=f'Привет,{subscription.user.username}',
            html_content=html_content,
        )
    except SMTPDataError:
        logging.exception('Ошибка при отправке сообщения')


def create_disposal_notification(subscription):
    try:
        box_number = subscription.box.number
        disposal_date = (datetime.now() + timedelta(30)).date
        html_content = f'''
                    <h1>Заберите вещи из бокса №{box_number}</h1>
                    <p>
                      Продлите аренду или заберите вещи до {disposal_date} иначе они будут уничтожены
                    </p>
                    '''

        send_email(
            f'Заберите вези из бокса №{box_number}',
            subscription.user.email,
            text_content=f'Привет,{subscription.user.username}',
            html_content=html_content,
        )
    except SMTPDataError:
        logging.exception('Ошибка при отправке сообщения')
