from django.contrib import admin

from .models import (
    Post,
    PostApplication,
)

admin.site.register(Post)
admin.site.register(PostApplication)

