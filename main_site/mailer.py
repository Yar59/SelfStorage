from django.core.mail import EmailMultiAlternatives

from self_storage.settings import EMAIL_HOST_USER


def send_email(subject, to, text_content='', html_content=''):
    msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_qr_link(qr_data):
    return f'https://api.qrserver.com/v1/create-qr-code/?data={qr_data}'
