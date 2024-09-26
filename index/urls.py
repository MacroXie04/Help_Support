# the urls.py for ranking

from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),

    path('register/', views.register, name='register'),



]