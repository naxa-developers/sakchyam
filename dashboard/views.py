from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, MilestoneYear, District, Municipality, Automation, Partner, AutomationPartner,FinancialLiteracy,\
    FinancialProgram
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.forms import LogDataForm, LogSubCategoryForm, LogCategoryForm, GroupForm, UserProfileForm, FinancialLiteracyForm,\
    AutomationForm, LogCategoryForm, PartnerForm, MilestoneYearForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group, Permission
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib import messages
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


class Dashboard(TemplateView):

    def get(self, request, *args, **kwargs):
        sidebar = LogCategory.objects.all()
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # group = Group.objects.get(user=user)
        # log = Log.objects.all().order_by('-id')
        # if group.name == 'admin':
        #     five = FiveW.objects.order_by('id')
        # else:
        #     five = FiveW.objects.select_related('supplier_id').filter(supplier_id=user_data.partner.id)[:10]
        return render(request, 'dashboard.html', {"sidebar": sidebar})


class LogCategoryList(LoginRequiredMixin, ListView):
    template_name = 'logcat_list.html'
    model = LogCategory

    def get_context_data(self, **kwargs):
        data = super(LogCategoryList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        query_data = LogCategory.objects.order_by('id')
        data['list'] = query_data
        return data


class LogCategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogCategory
    template_name = 'logcat_add.html'
    form_class = LogCategoryForm
    success_message = 'Log Category data created'

    def get_context_data(self, **kwargs):
        print('Log Cat')
        data = super(LogCategoryCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['active'] = 'logcat'
        data['years'] = {
            'y1': 'Year 1',
            'y2': 'Year 2',
            'y3': 'Year 3',
            'y4': 'Year 4',
            'y5': 'Year 5',
            'y6': 'Year 6',
            'y7': 'Year 7',
            'y8': 'Year 8',
            'y9': 'Year 9',
            'y10': 'Year 10'
        }
        return data

    def get_success_url(self):
        return reverse_lazy('logcat-list')


class AutomationList(LoginRequiredMixin, ListView):
    template_name = 'automation_list.html'
    model = Automation

    def get_context_data(self, **kwargs):
        data = super(AutomationList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        query_data = Automation.objects.order_by('id')
        data['list'] = query_data
        return data

class FinancialLiteracyList(LoginRequiredMixin, ListView):
    template_name = 'financialliteracy_list.html'
    model = FinancialLiteracy

    def get_context_data(self, **kwargs):
        data = super(FinancialLiteracyList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        query_data = FinancialLiteracy.objects.order_by('id')
        data['list'] = query_data
        return data


class AutomationCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Automation
    template_name = 'automation_create.html'
    form_class = AutomationForm
    success_message = 'Automation data created'

    def get_context_data(self, **kwargs):
        data = super(AutomationCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['provinces'] = Province.objects.order_by('id')
        data['districts'] = District.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        data['partners'] = Partner.objects.order_by('id')
        data['active'] = 'automation'
        return data

    def get_success_url(self):
        return reverse_lazy('automation-list')

class FinancialLiteracyCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = FinancialLiteracy
    template_name = 'financialliteracy_create.html'
    form_class = FinancialLiteracyForm
    success_message = 'FinancialLiteracy data created'

    def get_context_data(self, **kwargs):
        data = super(FinancialLiteracyCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['partner'] = Partner.objects.order_by('id')
        data['financialprogram'] = FinancialProgram.objects.order_by('id')
        data['active'] = 'automation'
        return data

    def get_success_url(self):
        return reverse_lazy('financialliteracy-list')

# class AutomationBulkCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
#     model = Automation
#     template_name = 'automation_create.html'
#     form_class = AutomationForm
#     success_message = 'Automation data created'

#     def get_context_data(self, **kwargs):
#         data = super(AutomationBulkCreate, self).get_context_data(**kwargs)
#         user = self.request.user
#         user_data = UserProfile.objects.get(user=user)
#         data['user'] = user_data
#         # data['active'] = 'program'
#         data['provinces'] = Province.objects.order_by('id')
#         data['districts'] = District.objects.order_by('id')
#         data['municipalities'] = Municipality.objects.order_by('id')
#         data['active'] = 'automation'
#         return data

#     def get_success_url(self):
#         return reverse_lazy('automation-list')


'''
This function enables creating the record of Sakchyam Partner model using a csv or xls file.
'''


def automationBulkCreate(request):
    template = 'automation_bulk_upload.html'

    # prompt = {
    #     'order': '''1. Please upload a .csv or .xls file \n
    #                 2. Order of the file columns should be Province, District, Municipality, Partner, Branch, No. of Tablets'''
    # }

    if request.method == "GET":
        return render(request, template)

    if request.method == 'POST':
        uploaded_file = request.FILES['autofile']

        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file).fillna('')
        elif uploaded_file.name.endswith(('.xls', 'xlsx')):
            df = pd.read_excel(uploaded_file).fillna('')
        else:
            messages.error(request, "Please upload a .csv or .xls file")

        upper_range = len(df)

        success_count = 0
        for row in range(0, upper_range):
            try:
                municipality = Municipality.objects.get(
                    code=df['Municipality'][row])
                province = municipality.province_id
                district = municipality.district_id
                partner = AutomationPartner.objects.get(
                    partner__code=df['Partner'][row])
                branch = None if df['Branch'][row] == '' else df['Branch'][row]
                numTablets = 0 if df['No. of Tablets'][row] == '' else df['No. of Tablets'][row]
                automation = Automation.objects.update_or_create(
                    province_id=province,
                    district_id=district,
                    municipality_id=municipality,
                    partner=partner,
                    branch=branch,
                    num_tablet_deployed=numTablets
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Automations Created ")
        return redirect('/dashboard/automation-list/', messages)


class AutomationEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Automation
    template_name = 'automation_edit.html'
    form_class = AutomationForm
    success_message = 'Automation data updated'

    def get_context_data(self, **kwargs):
        data = super(AutomationEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.order_by('id')
        data['districts'] = District.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        data['partners'] = Partner.objects.all()
        data['active'] = 'automation'
        return data

    def get_success_url(self):
        return reverse_lazy('automation-list')


class FinancialLiteracyEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = FinancialLiteracy
    template_name = 'financialliteracy_edit.html'
    form_class = FinancialLiteracyForm
    success_message = 'FinancialLiteracy data updated'

    def get_context_data(self, **kwargs):
        data = super(FinancialLiteracyEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['partner_type'] = Partner.objects.order_by('id')
        data['program_id'] = FinancialProgram.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        data['active'] = 'automation'
        return data

    def get_success_url(self):
        return reverse_lazy('financialliteracy-list')


class AutomationDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'automation_delete.html'
    success_message = 'Automation deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Automation, id=id)

    def get_success_url(self):
        return reverse_lazy('automation-list')

class FinancialLiteracyDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'financialliteracy_delete.html'
    success_message = 'FinancialLiteracy deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(FinancialLiteracy, id=id)

    def get_success_url(self):
        return reverse_lazy('financialliteracy-list')


class LogFrameList(LoginRequiredMixin, ListView):
    template_name = 'logframe_list.html'
    model = LogData

    def get_context_data(self, **kwargs):
        data = super(LogFrameList, self).get_context_data(**kwargs)
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        sidebar = LogCategory.objects.order_by('id')
        query_data = LogData.objects.filter(
            sub_category__id=self.kwargs['id']).order_by('id')
        data['list'] = query_data
        data['sidebar'] = sidebar
        return data


class LogSubCategoryList(LoginRequiredMixin, ListView):
    template_name = 'logsubcategory_list.html'
    model = LogSubCategory

    def get_context_data(self, **kwargs):
        data = super(LogSubCategoryList, self).get_context_data(**kwargs)
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        print()
        sidebar = LogCategory.objects.order_by('id')
        data['sidebar'] = sidebar
        query_data = LogSubCategory.objects.filter(
            category__id=self.kwargs['id']).order_by('id')
        data['list'] = query_data
        return data


class LogDataCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogData
    template_name = 'log_frame_add.html'
    form_class = LogDataForm
    success_message = 'Log data successfully Created'

    def get_context_data(self, **kwargs):
        data = super(LogDataCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        # data['active'] = 'program'
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['categories'] = LogCategory.objects.filter(
            id=self.kwargs['cat']).order_by('id')
        data['sub_categories'] = LogSubCategory.objects.filter(
            id=self.kwargs['subcat']).order_by('id')
        data['years'] = MilestoneYear.objects.order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logframe-list/' + str(self.kwargs['subcat'])


class LogSubCatCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogSubCategory
    template_name = 'logsubcat_add.html'
    form_class = LogSubCategoryForm
    success_message = 'Log data successfully Created'

    def get_context_data(self, **kwargs):
        data = super(LogSubCatCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        # data['active'] = 'program'
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['categories'] = LogCategory.objects.filter(
            id=self.kwargs['cat']).order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logsubcat-list/' + str(self.kwargs['cat'])


class LogSubCatUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LogSubCategory
    template_name = 'logsubcat_edit.html'
    form_class = LogSubCategoryForm
    success_message = 'Log data successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(LogSubCatUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        # data['active'] = 'program'
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['categories'] = LogCategory.objects.filter(
            id=self.kwargs['cat']).order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logsubcat-list/' + str(self.kwargs['cat'])


class LogDataUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LogData
    template_name = 'logdata_edit.html'
    form_class = LogDataForm
    success_message = 'Log data successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(LogDataUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        # data['active'] = 'program'
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['categories'] = LogCategory.objects.filter(
            id=self.kwargs['cat']).order_by('id')
        data['sub_categories'] = LogSubCategory.objects.filter(
            id=self.kwargs['subcat']).order_by('id')
        data['years'] = MilestoneYear.objects.order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logframe-list/' + str(self.kwargs['subcat'])


class UserList(LoginRequiredMixin, ListView):
    template_name = 'user_list.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        data = super(UserList, self).get_context_data(**kwargs)
        user_list = UserProfile.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['list'] = user_list
        data['user'] = user_data
        data['active'] = 'user'
        return data


class RoleList(LoginRequiredMixin, ListView):
    template_name = 'role_list.html'
    model = Group

    def get_context_data(self, **kwargs):
        data = super(RoleList, self).get_context_data(**kwargs)
        role_list = Group.objects.order_by('id')
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['list'] = role_list
        data['user'] = user_data
        data['active'] = 'permission'
        return data


def signup(request, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            UserProfile.objects.create(user=user, full_name=request.POST['full_name'], email=request.POST['email'],
                                       image=request.FILES['image'])
            return redirect('user')
        else:
            return render(request, 'create_user.html', {'form': form, })

    else:
        form = UserCreationForm()
        return render(request, 'create_user.html', {'form': form, })


class RoleCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'add_role.html'
    form_class = GroupForm
    success_message = 'Role successfully added'

    def get_context_data(self, **kwargs):
        data = super(RoleCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'role'
        data['permissions'] = Permission.objects.all()
        return data

    def get_success_url(self):
        return reverse_lazy('role')


class RoleUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'edit_role.html'
    form_class = GroupForm
    success_message = 'Role successfully added'

    def get_context_data(self, **kwargs):
        data = super(RoleUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'role'
        data['permissions'] = Permission.objects.all()
        return data

    def get_success_url(self):
        return reverse_lazy('role')


def create_role(request):
    if "GET" == request.method:
        permissions = Permission.objects.all()
        return render(request, 'add_role.html', {'permissions': permissions})

    else:
        role = request.POST['role']
        permission_list = request.POST.getlist('permissions')
        group = Group.objects.create(name=role)
        for permissions in permission_list:
            permission_check = Permission.objects.get(id=permissions)
            group.permissions.add(permission_check)

        return redirect('role')


def activate_user(request, **kwargs):
    user = User.objects.get(id=kwargs['id'])
    # user_data = UserProfile.objects.get(user=user)

    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect('user')


def assign_role(request, **kwargs):
    if "GET" == request.method:
        groups = Group.objects.all()
        user = request.user
        user_data = UserProfile.objects.get(user=user)
        return render(request, 'assign_role.html', {'user': user_data, 'groups': groups, 'user_id': kwargs['id']})
    else:
        user_id = request.POST['user']
        group_id = request.POST['group_id']
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        user.groups.add(group)
        # notify_message = user.username + ' was assigned ' + group.name + ' role by ' + request.user.username
        # notify = Notification.objects.create(user=user, message=notify_message, type='role',
        #                                      link='/dashboard/user-list')
        return redirect('user')


'''
Sakchyam Partner display list on dashboard
'''


class SakchyamAPartnersList(LoginRequiredMixin, ListView):
    template_name = 'sakchyam_partner_list.html'
    model = Partner

    def get_context_data(self, **kwargs):
        data = super(SakchyamAPartnersList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        query_data = Partner.objects.order_by('id')
        data['list'] = query_data
        return data


class SakchyamAPartnersCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Partner
    template_name = 'sakchyam_partners_create.html'
    form_class = PartnerForm
    success_message = 'Sakchyam Partner created'

    def get_context_data(self, **kwargs):
        data = super(SakchyamAPartnersCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-partners')


class SakchyamAPartnersEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Partner
    template_name = 'sakchyam_partner_edit.html'
    form_class = PartnerForm
    success_message = 'Sakchyam Partner data updated'

    def get_context_data(self, **kwargs):
        data = super(SakchyamAPartnersEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['active'] = 'program'
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-partners')


class SakchyamAPartnersDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'sakchyam_partner_delete.html'
    success_message = 'Sakchyam Partner deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Partner, id=id)

    def get_success_url(self):
        return reverse_lazy('sakchyam-partners')


'''
This function enables creating the record of Sakchyam Partner model using a csv or xls file.
'''


def sakchyamPartnerBulkCreate(request):
    template = 'sakchyam_bulk_upload.html'

    # prompt = {
    #     'order': '''1. Please upload a .csv or .xls file \n
    #                 2. Order of the file columns should be Name, Code'''
    # }

    if request.method == "GET":
        return render(request, template)

    if request.method == 'POST':
        uploaded_file = request.FILES['myfile']

        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file).fillna('')
        elif uploaded_file.name.endswith(('.xls', 'xlsx')):
            df = pd.read_excel(uploaded_file).fillna('')
        else:
            messages.error(request, "Please upload a .csv or .xls file")

        upper_range = len(df)

        success_count = 0
        for row in range(0, upper_range):
            try:
                name = df['Name'][row]
                if name == '' or name == 'NaN' or name == None:
                    messages.add_message(
                        request, messages.WARNING, "Data Format Error! Partner Number Missing for row " + str(row))
                    continue
                code = df['Code'][row]
                if code == '' or code == 'NaN' or code == None:
                    messages.add_message(
                        request, messages.WARNING, "Data Format Error! Partner Code Missing for row " + str(row))
                    continue
                partner = Partner.objects.update_or_create(
                    name=name,
                    code=code
                )
                success_count += 1
            except Exception as e:
                messages.add_message(request, messages.WARNING, str(e))
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Sakchyam Partners Created ")
        return redirect('/dashboard/sakchyam-partners/', messages)


class MilestoneYearCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = MilestoneYear
    template_name = 'milestone_year_create.html'
    form_class = MilestoneYearForm
    success_message = 'Milestone Year added'

    def get_context_data(self, **kwargs):
        data = super(MilestoneYearCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['years'] = {
            'y1': 'Year 1',
            'y2': 'Year 2',
            'y3': 'Year 3',
            'y4': 'Year 4',
            'y5': 'Year 5',
            'y6': 'Year 6',
            'y7': 'Year 7',
            'y8': 'Year 8',
            'y9': 'Year 9',
            'y10': 'Year 10'
        }
        data['user'] = user_data
        return data

    def get_success_url(self):
        return reverse_lazy('logcat-list')
