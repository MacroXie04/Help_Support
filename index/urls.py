# the urls.py for index
from django.template.defaulttags import csrf_token
from django.urls import path
from .views.static import index

from .views.api_csrf_token import get_csrf_token

urlpatterns = [

    # get csrf token
    path('csrf_token/', get_csrf_token, name='get_csrf_token'),


    # index
    path('', index, name='index'),

    # path('', views.index, name='index'),

    # path('help/', views.index_help, name='index_help'),

    # path('support/', views.index_support, name='index_support'),

    # path('add/', views.add_content, name='add_content'),

    # path('view_help/<content_id>/', views.view_help, name='view_help'),


]