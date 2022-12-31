from django.core.mail import send_mail
from random import randint
from django.conf import settings
import requests, json
from .models import User


def send_otp_via_email(email):
    subject = 'Your account verification email'
    otp = randint(1000, 9999)
    message = "Your OTP is {0}".format(otp)
    email_from = settings.EMAIL_HOST_USER
    print("mail send start")
    print(subject, message, email_from, [email])
    send_mail(subject, message, email_from, [email], fail_silently=False)
    print("success")
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
