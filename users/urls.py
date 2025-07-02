from django.urls import path
from users.views import webauthn
from users.views.webauthn import (
    web_login,
    web_register,
    web_logout,
)


app_name = 'users'

urlpatterns = [
    # webauthn views
    path('/login', web_login, name='web_login'),

    path('/register', web_login, name='web_register'),

    path('/logout', web_logout, name='web_logout'),
]