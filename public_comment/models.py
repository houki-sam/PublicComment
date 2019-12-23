from django.db import models
from django.core.validators import RegexValidator, slug_re
from django.utils import timezone


# Create your models here.

class Comment(models.Model):
    outline = models.CharField(max_length=1023) #見出し
    proposal_number_regex = RegexValidator(regex=r'^[0-9]+$', message = ("数字のみ利用できます。"))
    proposal_number = models.CharField(
        max_length=9,
        validators=[proposal_number_regex],
        primary_key = True,
        blank=False,
    )#案件番号
    title = models.CharField(max_length=511)#案件タイトル
    ground = models.CharField(max_length= 511)#法廷根拠
    low_or_optional = models.BooleanField(default=False)#True->法定 False->任意
    announcement_date = models.DateField()#公示日
    start_accepting = models.DateField(default = timezone.now) #意見・情報受付開始日
    deadline_date = models.DateField(default = timezone.now)#締切日
    append_date = models.DateTimeField(default= timezone.now)#データの追加日
    contact = models.CharField(max_length=511, blank=True)#連絡先
    url = models.URLField()#データのURL

    def __str__(self):
        return self.outline

class Category(models.Model):
    ministry = models.CharField(max_length=31, blank=True, null=True)#省
    agency = models.CharField(max_length=31, blank=True, null=True)#庁
    station = models.CharField(max_length=31, blank=True, null=True)#局
    post = models.ForeignKey(Comment, verbose_name='投稿詳細', on_delete=models.CASCADE)
    def __str__(self):
        return "/".join([self.ministry,self.agency,self.station])





