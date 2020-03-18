from django.contrib import admin
from api.models import LogCategory, LogSubCategory, LogData, MilestoneYear

# Register your models here.

admin.site.register(LogCategory)
admin.site.register(LogSubCategory)
admin.site.register(LogData)
admin.site.register(MilestoneYear)
# admin.site.register(Title)
