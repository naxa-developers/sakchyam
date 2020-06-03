from django.db import models


# Create your models here.

class Partner(models.Model):
    name = models.CharField(max_length=200)
    code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class AutomationPartner(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, related_name='AutoPartner')
    date = models.DateField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, default=0)
    longitude = models.FloatField(null=True, blank=True, default=0)
    beneficiary = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.partner.name


class LogCategory(models.Model):
    name = models.CharField(max_length=200)
    title = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class LogSubCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='Category')
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class MilestoneYear(models.Model):
    period = (
        ('y1', 'Year 1'),
        ('y2', 'Year 2'),
        ('y3', 'Year 3'),
        ('y4', 'Year 4'),
        ('y5', 'Year 5'),
        ('y6', 'Year 6'),
        ('y7', 'Year 7'),
        ('y8', 'Year 8'),
        ('y9', 'Year 9'),
        ('y10', 'Year 10'),
    )
    period = models.CharField(max_length=30, blank=True, null=True, choices=period)
    name = models.CharField(max_length=200, null=True, blank=True)
    range = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


# class Title(models.Model):
#     title = models.CharField(max_length=500)
#     source = models.CharField(max_length=500, null=True, blank=True)
#     sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='TitleSubCat')
#     description = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return self.title


class LogData(models.Model):
    DATA_TYPE = (
        ('number', 'Number'),
        ('budget', 'Budget'),
        ('percentage', 'Percentage'),
    )

    UNIT = (
        ('pound', 'Pound'),
        ('rupees', 'Rupees'),
    )

    # title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='LogTitle', blank=True, null=True)
    data_type = models.CharField(max_length=30, choices=DATA_TYPE, blank=True, null=True)
    planned_afp = models.CharField(max_length=30, blank=True, null=True, default=0)
    achieved = models.CharField(max_length=30, blank=True, null=True, default=0)
    year = models.ForeignKey(MilestoneYear, on_delete=models.CASCADE, related_name='LogYear')
    sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='LogSubCat')
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='LogCat')
    unit = models.CharField(max_length=30, blank=True, null=True, choices=UNIT)
    is_related = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category.name


class Province(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class District(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='DistrictProvince', null=True,
                                    blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.IntegerField(default=0)
    n_code = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='MunProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='MunDistrict', null=True,
                                    blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    municipality_type = models.CharField(max_length=100, null=True, blank=True)
    hlcit_code = models.CharField(max_length=100, null=True, blank=True)
    code = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Automation(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='AutoProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='AutoDistrict', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='AutoMunicipality',
                                        null=True,
                                        blank=True)
    partner = models.ForeignKey(AutomationPartner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                related_name='PartnerAuto')
    branch = models.CharField(max_length=100, null=True, blank=True)
    num_tablet_deployed = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.branch


class FinancialProgram(models.Model):
    name = models.CharField(max_length=200)
    code = models.IntegerField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    total = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


class FinancialLiteracy(models.Model):
    type = (
        ('Microfinance Institutions', 'Microfinance Institutions'),
        ('Commercial Bank and Other Partners', 'Commercial Bank and Other Partners'),
    )

    partner_type = models.CharField(max_length=200, blank=True, null=True, choices=type)
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='PartnerFinancial')
    program_id = models.ForeignKey(FinancialProgram, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='ProgramFinancial')
    value = models.IntegerField(blank=True, null=True, default=0)
    single_count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.partner_type
