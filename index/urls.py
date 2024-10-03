# the urls.py for index

from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index'),

    path('help/', views.index_help, name='index_help'),

    path('support/', views.index_support, name='index_support'),

    path('add_help_content/', views.add_help_content, name='add_help_content'),

    path('add_support_content/', views.add_support_content, name='add_support_content'),


]