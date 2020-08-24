from rest_framework import serializers
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, \
    Automation, FinancialProgram, FinancialLiteracy, Project, Partner, Partnership, Product, ProductProcess, \
    SecondaryData, Payment


class LogCategorySerializer(serializers.ModelSerializer):
    subcat = serializers.SerializerMethodField()

    class Meta:
        model = LogCategory
        fields = ('id', 'name', 'title', 'subcat')

    def get_subcat(self, obj):
        qs = obj.Category.all().order_by('id').values('id', 'name', 'title', 'description')
        return qs


class LogSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSubCategory
        fields = '__all__'
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'investment_primary')


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'


class PartnershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partnership
        fields = '__all__'


class MilestoneYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilestoneYear
        fields = '__all__'


class FinancialProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProgram
        fields = '__all__'


class FinancialLiteracySerializer(serializers.ModelSerializer):
    partner_type = serializers.SerializerMethodField()

    class Meta:
        model = FinancialLiteracy
        fields = ('id', 'partner_id', 'partner_type', 'program_id', 'value', 'single_count')

    def get_partner_type(self, obj):
        partner_id = obj.partner_id.financial_literacy
        return partner_id


class FinancialPartnerSerializer(serializers.ModelSerializer):
    partner_name = serializers.SerializerMethodField()
    partner_type = serializers.SerializerMethodField()

    class Meta:
        model = FinancialLiteracy
        fields = ('id', 'partner_id', 'partner_type', 'partner_name',)

    def get_partner_name(self, obj):
        partner_id = obj.partner_id.name
        return partner_id

    def get_partner_type(self, obj):
        partner_id = obj.partner_id.financial_literacy
        return partner_id


class ProductSerializer(serializers.ModelSerializer):
    # partner_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    # def get_partner_name(self, obj):
    #     partner_id = obj.partner_id.name
    #     return partner_id


class SecondarySerializer(serializers.ModelSerializer):
    province_code = serializers.SerializerMethodField()
    district_code = serializers.SerializerMethodField()
    municipality_code = serializers.SerializerMethodField()
    province_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    municipality_name = serializers.SerializerMethodField()

    class Meta:
        model = SecondaryData
        fields = ('id', 'province_code', 'district_code', 'municipality_code', 'hdi', 'head_quarter', 'population',
                  'yearly_fund', 'social_security_recipients',
                  'province_name',
                  'district_name',
                  'municipality_name',
                  'yearly_social_security_payment',
                  'nearest_branch_distance',
                  'communication_landline',
                  'communication_mobile',
                  'communication_internet',
                  'communication_internet_other',
                  'available_electricity_maingrid',
                  'available_electricity_micro_hydro',
                  'nearest_road_location_name',
                  'nearest_road_distance',
                  'nearest_road_type',
                  'nearest_police_location_name',
                  'nearest_police_distance',
                  'categorisation_by_sakchyam'
                  )

    def get_province_code(self, obj):
        code = obj.province_id.code
        return code

    def get_district_code(self, obj):
        code = obj.district_id.n_code
        return code

    def get_municipality_code(self, obj):
        code = obj.municipality_id.code
        return code

    def get_province_name(self, obj):
        name = obj.province_id.name
        return name

    def get_district_name(self, obj):
        name = obj.district_id.name
        return name

    def get_municipality_name(self, obj):
        name = obj.municipality_id.name
        return name


class ProductProcessSerializer(serializers.ModelSerializer):
    partner_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    product_category = serializers.SerializerMethodField()
    partner_type = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = ProductProcess
        fields = (
            'id', 'partner_id', 'partner_name', 'partner_type', 'product_id', 'product_name', 'date',
            'product_category',
            'innovation_area',
            'market_failure')

    def get_date(self, obj):
        date = obj.product_id.date
        return date

    def get_partner_name(self, obj):
        partner_id = obj.partner_id.name
        return partner_id

    def get_partner_type(self, obj):
        partner_id = obj.partner_id.product_process
        return partner_id

    def get_product_name(self, obj):
        partner_id = obj.product_id.name
        return partner_id

    def get_product_category(self, obj):
        partner_id = obj.product_id.type
        return partner_id


class LogDataSerializer(serializers.ModelSerializer):
    year = serializers.ReadOnlyField(source='year.year')
    sub_category = serializers.ReadOnlyField(source='sub_category.name')
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = LogData
        fields = ['id', 'planned_afp', 'achieved', 'year', 'category', 'sub_category']


class LogDataAlternativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogData
        fields = '__all__'
        depth = 1


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    province_code = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = fields = ('id', 'name', 'n_code', 'province_code', 'code')

    def get_province_code(self, obj):
        code = obj.province_id.code
        return code


class MunicipalitySerializer(serializers.ModelSerializer):
    province_code = serializers.SerializerMethodField()
    district_code = serializers.SerializerMethodField()

    class Meta:
        model = Municipality
        fields = ('id', 'name', 'district_code', 'province_code', 'code')

    def get_district_code(self, obj):
        code = obj.district_id.n_code
        return code

    def get_province_code(self, obj):
        code = obj.province_id.code
        return code


class AutomationSerializer(serializers.ModelSerializer):
    partner_id = serializers.SerializerMethodField()
    mun_code = serializers.SerializerMethodField()

    class Meta:
        model = Automation
        fields = (
            'id', 'partner_id', 'partner', 'branch', 'province_id', 'district_id', 'municipality_id',
            'num_tablet_deployed', 'mun_code',)

    def get_partner_id(self, obj):
        partner_id = obj.partner.partner.id
        return partner_id

    def get_mun_code(self, obj):
        code = obj.municipality_id.code
        return code


class PaymentSerial(serializers.ModelSerializer):
    direct_links = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id', 'component', 'direct_links', 'indirect_links', 'link_with_indirect', 'description', 'title',
                  'component_value')

    def get_direct_links(self, obj):
        data = []
        qs = obj.direct_links.all().values('components')
        for q in qs:
            data.append(
                q['components']
            )
        return data
