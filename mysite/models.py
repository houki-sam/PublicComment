from django.db import models
from django.utils import timezone

class ContactModel(models.Model):
    fullname = models.CharField(
            verbose_name = '名前',
            blank = False,
            null = False,
            max_length = 50,
            default='',
            )

    subject = models.CharField(
            verbose_name = '件名',
            blank = False,
            null = False,
            max_length = 100,
            default='',
            )

    email = models.EmailField(
            verbose_name ='メールアドレス',
            blank = False,
            null = False,
            max_length = 100,
            default = '',
            )

    messages = models.TextField(
            verbose_name = '本文',
            blank = False,
            null = False,
            default = '',
            )

    published_date = models.DateTimeField(
            verbose_name = '日時',
            blank = True,
            null = False,
            )

    def save_form(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.subject
