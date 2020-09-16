from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class Partner(models.Model):
    types = (
        ('Microfinance Institutions/Cooperatives', 'Microfinance Institutions/Cooperatives'),
        ('Commercial Bank and Other Partners', 'Commercial Bank and Other Partners'),
    )

    n_types = (
        ('Microfinance/Cooperative', 'Microfinance/Cooperative'),
        ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'),
        ('Commercial Bank', 'Commercial Bank'),
        ('Microfinance', 'Microfinance'),
        ('Digital Financial Service Providers', 'Digital Financial Service Providers'),
        ('Cooperative', 'Cooperative'),
        ('Digital Financial Service Operator', 'Digital Financial Service Operator'),
        ('Insurance Provider', 'Insurance Provider'),
        ('Apex Organization', 'Apex Organization'),
        ('Mobile Network Operator', 'Mobile Network Operator'),
        ('Insurance', 'Insurance'),
    )

    name = models.CharField(max_length=200)
    code = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True, choices=types)
    financial_literacy = models.CharField(max_length=200, blank=True, null=True, choices=n_types)
    partnership = models.CharField(max_length=200, blank=True, null=True, choices=n_types)
    outreach_expansion = models.CharField(max_length=200, blank=True, null=True, choices=n_types)
    mfs = models.CharField(max_length=200, blank=True, null=True, choices=n_types)
    product_process = models.CharField(max_length=200, blank=True, null=True, choices=n_types)

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
    yearname = models.CharField(max_length=50, blank=True, null=True)

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
    data_type = models.CharField(max_length=300, blank=True, null=True)
    planned_afp = models.CharField(max_length=30, blank=True, null=True, default=0)
    achieved = models.CharField(max_length=30, blank=True, null=True, default=0)
    year = models.ForeignKey(MilestoneYear, on_delete=models.CASCADE, related_name='LogYear')
    sub_category = models.ForeignKey(LogSubCategory, on_delete=models.CASCADE, related_name='LogSubCat')
    category = models.ForeignKey(LogCategory, on_delete=models.CASCADE, related_name='LogCat')
    unit = models.CharField(max_length=30, blank=True, null=True, )
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
        ('Microfinance/Cooperative', 'Microfinance/Cooperative'),
        ('Commercial Banks and Mobile Network Operators', 'Commercial Banks and Mobile Network Operators'),
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


class Project(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, )
    code = models.CharField(max_length=500, blank=True, null=True, )
    investment_primary = models.CharField(max_length=500, blank=True, null=True, )
    investment_secondary = models.CharField(max_length=500, blank=True, null=True, )
    leverage = models.BigIntegerField(blank=True, null=True, default=0)
    scf_funds = models.BigIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


class Partnership(models.Model):
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='PartnerPart')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='ProjectPartner')
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='PartProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='PartDistrict', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='PartMunicipality',
                                        null=True,
                                        blank=True)
    branch = models.IntegerField(blank=True, null=True, default=0)
    blb = models.IntegerField(blank=True, null=True, default=0)
    extension_counter = models.IntegerField(blank=True, null=True, default=0)
    tablet = models.IntegerField(blank=True, null=True, default=0)
    other_products = models.IntegerField(blank=True, null=True, default=0)
    beneficiary = models.IntegerField(blank=True, null=True, default=0)
    scf_funds = models.IntegerField(blank=True, null=True, default=0)
    allocated_budget = models.FloatField(blank=True, null=True, default=0)
    allocated_beneficiary = models.FloatField(blank=True, null=True, default=0)
    female_percentage = models.FloatField(blank=True, null=True, default=0)
    total_beneficiary = models.IntegerField(blank=True, null=True, default=0)
    female_beneficiary = models.IntegerField(blank=True, null=True, default=0)
    status = models.CharField(max_length=500, blank=True, null=True, )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project_year = models.CharField(max_length=500, blank=True, null=True, )


class Product(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, )
    type = models.CharField(max_length=500, blank=True, null=True, )
    code = models.IntegerField(blank=True, null=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductProcess(models.Model):
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='ProcessProduct')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='ProcessProduct')
    partner_type = models.CharField(max_length=500, blank=True, null=True, )
    innovation_area = models.CharField(max_length=500, blank=True, null=True, )
    market_failure = models.CharField(max_length=500, blank=True, null=True, )

    def __str__(self):
        return self.innovation_area


class SecondaryData(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='SecondProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='SecondDistrict', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='SecondMunicipality',
                                        null=True,
                                        blank=True)
    hdi = models.FloatField(blank=True, null=True)
    head_quarter = models.CharField(max_length=500, blank=True, null=True, )
    population = models.IntegerField(blank=True, null=True)
    yearly_fund = models.FloatField(blank=True, null=True)
    social_security_recipients = models.IntegerField(blank=True, null=True)
    yearly_social_security_payment = models.FloatField(blank=True, null=True)
    nearest_branch_distance = models.FloatField(blank=True, null=True)
    communication_landline = models.CharField(max_length=500, blank=True, null=True, )
    communication_mobile = models.CharField(max_length=500, blank=True, null=True, )
    communication_internet = models.CharField(max_length=500, blank=True, null=True, )
    communication_internet_other = models.CharField(max_length=500, blank=True, null=True, )
    available_electricity_maingrid = models.CharField(max_length=500, blank=True, null=True, )
    available_electricity_micro_hydro = models.CharField(max_length=500, blank=True, null=True, )
    nearest_road_location_name = models.CharField(max_length=500, blank=True, null=True, )
    nearest_road_distance = models.FloatField(blank=True, null=True)
    nearest_road_type = models.CharField(max_length=500, blank=True, null=True, )
    nearest_police_location_name = models.CharField(max_length=500, blank=True, null=True, )
    nearest_police_distance = models.FloatField(blank=True, null=True)
    categorisation_by_sakchyam = models.CharField(max_length=500, blank=True, null=True, )


class Outreach(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='OutProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='OutDistrict', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='OutMunicipality',
                                        null=True,
                                        blank=True)
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='OutreachPartner')
    partner_type = models.CharField(max_length=500, blank=True, null=True, )
    market_name = models.CharField(max_length=500, blank=True, null=True, )
    expansion_driven_by = models.CharField(max_length=500, blank=True, null=True, )
    point_service = models.CharField(max_length=500, blank=True, null=True, )
    date_established = models.DateField(null=True, blank=True)
    g2p_payment = models.CharField(max_length=500, blank=True, null=True, )
    demonstration_effect = models.CharField(max_length=500, blank=True, null=True, )
    gps_point = models.CharField(max_length=500, blank=True, null=True, )

    def __str__(self):
        return self.expansion_driven_by


class MFS(models.Model):
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='MFProvince', null=True,
                                    blank=True)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name='MFDistrict', null=True,
                                    blank=True)
    municipality_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='MFMunicipality',
                                        null=True,
                                        blank=True)
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='MFPartner')
    key_innovation = models.CharField(max_length=500, blank=True, null=True, )
    achievement_type = models.CharField(max_length=500, blank=True, null=True, )
    achieved_number = models.IntegerField(blank=True, null=True)


class Insurance(models.Model):
    partner_id = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                   related_name='InPartner')
    distribution_channel = models.CharField(max_length=500, blank=True, null=True, )
    innovation = models.CharField(max_length=500, blank=True, null=True, )
    product = models.CharField(max_length=500, blank=True, null=True, )
    description = models.TextField(blank=True, null=True)
    number_of_insurance_sold = models.IntegerField(blank=True, null=True, default=0)
    amount_of_insurance = models.FloatField(blank=True, null=True, default=0)
    amount_of_sum_insuranced = models.FloatField(blank=True, null=True, default=0)
    amount_of_claim = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return self.product


class DirectLink(models.Model):
    type = (
        ('RTGS', 'RTGS'),
        ('National Switch', 'National Switch'),
        ('CSD', 'CSD'),
        ('Card and Switch System', 'Card and Switch System'),
        ('PSPs/PSOs', 'PSPs/PSOs'),
        ('NCHL', 'NCHL'),
        ('BFIS', 'BFIS'),
        ('Capital Market Players', 'Capital Market Players'),
    )
    components = models.CharField(max_length=500, choices=type)

    def __str__(self):
        return self.components


class Payment(models.Model):
    type = (
        ('RTGS', 'RTGS'),
        ('National Switch', 'National Switch'),
        ('CSD', 'CSD'),
        ('Card and Switch System', 'Card and Switch System'),
        ('PSPs/PSOs', 'PSPs/PSOs'),
        ('NCHL', 'NCHL'),
        ('BFIS', 'BFIS'),
        ('Capital Market Players', 'Capital Market Players'),
    )

    component = models.CharField(max_length=500, choices=type)
    indirect_links = models.CharField(max_length=500,choices=type,blank=True,null=True)
    link_with_indirect = models.CharField(max_length=500,choices=type,blank=True,null=True)
    direct_links = models.ManyToManyField(DirectLink,blank=True,null=True)
    description = RichTextField(blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    component_value = models.CharField(max_length=100,blank=True,null=True)




