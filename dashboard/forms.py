from django.forms import ModelForm
from api.models import LogData, LogCategory, LogSubCategory, MilestoneYear


class LogCategoryForm(ModelForm):
    class Meta:
        model = LogCategory
        fields = '__all__'


class LogDataForm(ModelForm):
    class Meta:
        model = LogData
        fields = '__all__'


class LogSubCategoryForm(ModelForm):
    class Meta:
        model = LogSubCategory
        fields = '__all__'


class MilestoneYearForm(ModelForm):
    class Meta:
        model = MilestoneYear
        fields = '__all__'

# class TitleForm(ModelForm):
#     class Meta:
#         model = Title
#         fields = '__all__'
