from anaconda_cloud_auth.client import login_required
from django.urls import path
from postings.views import (
    index,
    post,
)


app_name = 'postings'

urlpatterns = [
    path("", index.post_list, name='index'),

    path('create/', post.create_post, name='create_post'),

    path("post/<uuid:uuid>/", post.post_detail, name="post_detail"),

    # URL for updating a post (you will need to create the template for this)
    path('post/<uuid:uuid>/edit/', post.post_update, name='post_update'),

    # URL for deleting a post
    path('post/<uuid:uuid>/delete/', post.post_delete, name='post_delete'),
]