from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config.celery_app import app


@app.task
def send_order_email(instance):
    subject = 'Order'
    html_message = render_to_string('templates/email_template.html', {'instance': instance})
    plain_message = strip_tags(html_message)
    sender = 'eStore@estore.com'
    receiver = instance.email
    send_mail(
        subject,
        plain_message,
        sender,
        receiver,
        html_message=html_message,
        fail_silently=False,
    )
