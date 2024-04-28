from django.core.mail import send_mail
from django.conf import settings


def send_email(subject: str, body: str, recipient_list: list):
    try:
        import smtplib

        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        username = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        sender = settings.DEFAULT_FROM_EMAIL
        subject = subject
        body = body

        for recipient in recipient_list:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
                smtp.login(username, password)
                smtp.sendmail(sender, recipient, body)

        return 1
    except Exception as ex:
        return 0