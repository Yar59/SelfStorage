from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(subject, to, text_content='', html_content=''):
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_qr_link(qr_data):
    return f'https://api.qrserver.com/v1/create-qr-code/?data={qr_data}'
