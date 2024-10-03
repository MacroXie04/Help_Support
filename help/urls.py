# Description: This file is used to define the URL patterns for the help app.
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('accounts/admin/', admin.site.urls),

    # index
    path('', include('index.urls')),

    # account
    path('account/', include('account.urls')),

    # chat
    path('chat/', include('chat.urls')),

]
