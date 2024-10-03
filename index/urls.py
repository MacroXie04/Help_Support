# the urls.py for index

from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name='index'),

    path('content/<int:content_id>/', views.content, name='content'),

    path('add/', views.add_content, name='add_content'),

]