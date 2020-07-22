from django.contrib import admin
from api.models import LogCategory, LogSubCategory, LogData, MilestoneYear, Province, Municipality, Automation, \
    District, Partner, AutomationPartner, FinancialProgram, FinancialLiteracy, Project, Partnership, Product, \
    ProductProcess, SecondaryData

# Register your models here.

admin.site.register(LogCategory)
admin.site.register(LogSubCategory)
admin.site.register(LogData)
admin.site.register(MilestoneYear)
admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Automation)
admin.site.register(District)
admin.site.register(Partner)
admin.site.register(AutomationPartner)
admin.site.register(FinancialProgram)
admin.site.register(FinancialLiteracy)
admin.site.register(Project)
admin.site.register(Partnership)
admin.site.register(Product)
admin.site.register(ProductProcess)
admin.site.register(SecondaryData)
