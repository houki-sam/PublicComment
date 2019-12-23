import datetime

import environ

from django.db.models import Q
from django.shortcuts import render
from django.core.mail import BadHeaderError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils import timezone, dateformat
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View
from .forms import DetailSearch
from .models import Comment



# Create your views here.

@login_required
def index(request):
    time = timezone.now()
    time_str = dateformat.format(time, "Y年n月d日")
    result = Comment.objects.filter(announcement_date=time)
    form = {
        "result" : result,
        "date" : time_str,
    }
    return render(request,"public_comment/index.html",form)


@login_required
def detail(request, *args, **kwargs):
    form = DetailSearch(request.GET)
    if "title" in request.GET:
        result = Comment.objects.filter(
            title__icontains= request.GET["title"]
        )
    else:
        result = None
    context = {
        "title":"キーワードから検索",
        "form":form, 
        "result":result,    
    }
    return render(request,"public_comment/detail.html",context)

@login_required
def agency(request, *args, **kwargs):
    form = DetailSearch(request.GET)
    if "title" in request.GET:
        result = Comment.objects.filter(
            contact__icontains= request.GET["title"]
        )
    else:
        result = None
    context = {
        "title":"省庁から検索",
        "form":form, 
        "result":result,    
    }
    return render(request,"public_comment/detail.html",context)
        

    
       

