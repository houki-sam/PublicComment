from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


def sender():
    data = User.objects.all()
    email_list = [x.email for x in data]

    """題名"""
    subject = "題名"
    """本文"""
    message = "本文です\nこんにちは。メールを送信しました"
    """送信元メールアドレス"""
    from_email = "legal.dsone@gmail.com"
    """宛先メールアドレス"""
    recipient_list = email_list

    send_mail(subject, message, from_email, recipient_list)
