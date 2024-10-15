# the urls.py for account
from django.urls import path
from account import views

urlpatterns = [
    path('login/', views.web_login, name='login'),

    path('logout/', views.web_logout, name='logout'),

    path('register/', views.web_register, name='register'),

    path('account_disabled/', views.account_disabled, name='account_disabled'),





]