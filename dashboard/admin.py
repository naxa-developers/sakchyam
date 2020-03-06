from django.contrib import admin
from dashboard.models import UserRole
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(UserRole)
admin.site.register(Permission)
