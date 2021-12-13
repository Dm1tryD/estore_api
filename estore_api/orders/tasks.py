from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config.celery_app import app


@app.task
def send_order_email(order):
    subject = 'Order'
    html_message = render_to_string(
        'email_template.html', {'order': order, 'order_items': order.order_items.all()}
    )
    plain_message = strip_tags(html_message)
    sender = 'eStore@estore.com'
    receiver = [order.email, ]
    send_mail(
        subject,
        plain_message,
        sender,
        receiver,
        html_message=html_message,
        fail_silently=False,
    )
