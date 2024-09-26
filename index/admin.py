from django.contrib import admin

# Register your models here.

from .models import Content, UserProfile

admin.site.register(Content)