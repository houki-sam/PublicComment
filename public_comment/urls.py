"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "search"

urlpatterns = [
    path('',views.index,name="index"), 
    path('keyword',views.detail,name="detail"),
    path('keyword/<str:title>/',views.detail,name="detail_result"),
    path('agency',views.agency,name="agency"),
    
    path('agency/<str:title>/',views.agency,name="agency_result"),
    
]
