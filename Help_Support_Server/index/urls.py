from django.urls import path
from .views.index import layout


urlpatterns = [
    path('layout/', layout, name='layout'),

]