from django.forms import ModelForm
from django.contrib.auth.models import User, Permission, Group
from api.models import LogData, LogCategory, LogSubCategory, MilestoneYear, Automation, Partner
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


class AutomationForm(ModelForm):
    class Meta:
        model = Automation
        fields = '__all__'
        # labels = {
        #     'province_id': 'Province'
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['province_id'].widget.attrs.update({'class': 'col-md-6 form-group selectpicker'})

class PartnerForm(ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'
