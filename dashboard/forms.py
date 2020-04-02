from django.forms import ModelForm
from django.contrib.auth.models import User, Permission, Group
from api.models import LogData, LogCategory, LogSubCategory, MilestoneYear
from .models import UserProfile


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


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
