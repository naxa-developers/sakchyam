from django.contrib import admin
from api.models import LogCategory, LogSubCategory, LogData, MilestoneYear, Province, Municipality, Automation, District

# Register your models here.

admin.site.register(LogCategory)
admin.site.register(LogSubCategory)
admin.site.register(LogData)
admin.site.register(MilestoneYear)
admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Automation)
admin.site.register(District)
