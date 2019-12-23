from django.urls import path, include
from . import views

# Create your views here.

app_name = "accounts"

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

]
