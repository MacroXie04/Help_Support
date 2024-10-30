# the urls.py for account
from django.urls import path
from account.views.api_login import api_login
from account.views.api_register import api_register
from account.views.api_logout import api_logout
from account.views.api_user_info import api_user_info, user_info_short
from account.views.static import web_login, web_register, web_account_disable, web_account_page, web_logout

urlpatterns = [
    # static pages
    path('login/', web_login, name='login'),
    path('logout/', web_logout, name='logout'),
    path('register/', web_register, name='register'),

    path('account_disabled/', web_account_disable, name='account_disabled'),

    path('account_page', web_account_page, name='account_page'),


    #     path('register/', views.web_register, name='register'),

    #     path('manage/', views.account_page, name='account_page'),

    #     path('add_balance/', views.add_balance, name='add_balance'),

    #     path('account_disabled/', views.account_disabled, name='account_disabled'),

    # api endpoints
    path('api/login/', api_login, name='api_login'),

    path('api/register/', api_register, name='api_register'),

    path('api/logout/', api_logout, name='api_logout'),

    path('api/user_info/', api_user_info, name='api_user_info'),

    path('api/user_info_short/', user_info_short, name='user_info_short'),
]
