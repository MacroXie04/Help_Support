# the urls.py for account
from django.urls import path
from account import views

urlpatterns = [
    path('login/', views.web_login, name='login'),

    path('register/', views.web_register, name='register'),

    path('account_disabled/', views.account_disabled, name='account_disabled'),

    path('logout/', views.web_logout, name='logout'),

    path('profile/', views.profile, name='profile'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('account/profile/edit/password/', views.profile_edit_password, name='profile_edit_password'),

    path()



]