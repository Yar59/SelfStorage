from django.core.management import BaseCommand
from django.conf import settings

from main_site.mailer import *
from main_site.models import *


class Command(BaseCommand):
    help = 'Запустите для рассылки сообщений на почту'

    def handle(self, *args, **kwargs):
        pass
