from django.core.mail import send_mail
from config.celery_app import app


@app.task
def send_email(data):
    send_mail(
        data['email_subject'],
        data['email_body'],
        'eStore@estore.com',
        [data['to_email']],
        fail_silently=False,
    )
