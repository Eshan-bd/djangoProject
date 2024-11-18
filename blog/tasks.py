from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode

from blog.constants import NO_REPLY_EMAIL_ADDRESS
from blog.models import BlogPost


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
        NO_REPLY_EMAIL_ADDRESS,
        ['testmojo@yopmail.com'],
        fail_silently=False,
        html_message=message  # Specify the HTML content here
    )

@shared_task
def send_weekly_email_to_users():
    # Get the current date and the start of the current week
    today = timezone.now()
    start_of_week = today - timezone.timedelta(days=today.weekday())  # Start of this week (Monday)

    # Get all users
    users = User.objects.all()

    for user in users:
        # Get posts made by the user during the week
        posts = BlogPost.objects.filter(author=user, created_at__gte=start_of_week)

        if posts.exists():
            # Prepare the subject and message
            subject = 'Your Weekly Update'
            message = render_to_string('email/weekly_update.html', {
                'user': user,
                'posts': posts,
            })

            # Send email
            send_mail(
                subject,
                message,
                NO_REPLY_EMAIL_ADDRESS,  # Sender email
                [user.email],
                html_message=message  # Send HTML email
            )

    return f'Weekly email sent to {len(users)} users.'
