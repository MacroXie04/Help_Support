"""
URL configuration for Help_Support project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Help_Support.settings import WEB_ADMIN

urlpatterns = [
    path('', include('postings.urls')),

    path('webauthn/', include('users.urls')),

    path('chat/', include('chat.urls')),
]

if WEB_ADMIN:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

