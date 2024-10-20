# the urls.py for account
from django.urls import path
from account import views

urlpatterns = [
    path('login/', views.web_login, name='login'),

    path('logout/', views.web_logout, name='logout'),

    path('register/', views.web_register, name='register'),

    path('manage/', views.account_page, name='account_page'),

    path('add_balance/', views.add_balance, name='add_balance'),

    path('account_disabled/', views.account_disabled, name='account_disabled'),






]