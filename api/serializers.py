from rest_framework import serializers
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData


class LogCategorySerializer(serializers.ModelSerializer):
    subcat = serializers.SerializerMethodField()

    class Meta:
        model = LogCategory
        fields = ('id', 'name', 'title', 'subcat')

    def get_subcat(self, obj):
        qs = obj.Category.all().order_by('id').values('id', 'name')
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

# class TitleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Title
#         fields = '__all__'
