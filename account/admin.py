from django.contrib import admin
from .models import UserProfile
from .models import AccountBalance


admin.site.register(UserProfile)
admin.site.register(AccountBalance)

