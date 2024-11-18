from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode


@shared_task
def send_confirmation_email(user_id, user_email):
    user = User.objects.get(id=user_id)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.id).encode())
    domain = 'localhost:8000'
    link = f"http://{domain}/confirm-email/{uid}/{token}/"

    subject = 'Email Confirmation'
    message = render_to_string('email/confirmation_email.html', {
        'user': user,
        'link': link,
    })
    send_mail(
        subject,
        message,
        'noreply@yourdomain.com',
        ['testmojo@yopmail.com'],
        fail_silently=False,
        html_message=message  # Specify the HTML content here
    )
