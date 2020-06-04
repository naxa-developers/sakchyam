from rest_framework import serializers
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, \
    Automation, FinancialProgram, FinancialLiteracy


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


class MilestoneYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilestoneYear
        fields = '__all__'


class FinancialProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProgram
        fields = '__all__'


class FinancialLiteracySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialLiteracy
        fields = '__all__'


class FinancialPartnerSerializer(serializers.ModelSerializer):
    partner_name = serializers.SerializerMethodField()

    class Meta:
        model = FinancialLiteracy
        fields = ('id', 'partner_id', 'partner_type', 'partner_name',)

    def get_partner_name(self, obj):
        partner_id = obj.partner_id.name
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
    class Meta:
        model = District
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'


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
