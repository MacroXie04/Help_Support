from anaconda_cloud_auth.client import login_required
from django.urls import path
from postings.views import (
    index,
    post,
)


app_name = 'postings'

urlpatterns = [
    path("", index.index_page, name='index'),

    path('create/', post.create_post, name='create_post'),
]