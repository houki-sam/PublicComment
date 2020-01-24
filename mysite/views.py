from django.shortcuts import render
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.http import HttpResponse
from public_comment.models import Comment
from django.utils import timezone
from django.views.generic import View
from .forms import ContactForm
from django.db.models import Max
from .settings import DEFAULT_EMAIL
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

# Create your views here.


class Home(View):
    #@login_required
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form,
        }
        return render(request, "mysite/homepage.html", context)

    #@login_required
    def post(self, request, *args, **kwargs):
        subject = "問い合わせ パブリックコメント"
        message = "問い合わせがありました。<br>名前:{}<br>メールアドレス:{}<br>問い合わせ内容:<br>{}".format(
            request.POST['name'], request.POST['email'], request.POST['message'])
        from_email = DEFAULT_EMAIL  # 送信者
        recipient_list = ["mojamoja.bstgs.0626@gmail.com"]  # 宛先リスト
        bcc = []  # BCCリ
        email = EmailMessage(subject, message, from_email, recipient_list, bcc)
        email.send()
        form = ContactForm()
        context = {
            "form": form,
            "message": "送信が完了しました",
            "sub_message": "返信いたしますのでもう少々お待ちください。"
        }
        return render(request, "mysite/homepage.html", context)
