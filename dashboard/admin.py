from django.contrib import admin
from dashboard.models import UserProfile
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Permission)
