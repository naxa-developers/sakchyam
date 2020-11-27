from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, MilestoneYear, District, \
    Municipality, Automation, Partner, AutomationPartner, FinancialLiteracy, \
    FinancialProgram, Outreach, ProductProcess, Product, Project, AutomationPartner, MFS, Insurance, SecondaryData, \
    Partnership
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.forms import LogDataForm, LogSubCategoryForm, LogCategoryForm, GroupForm, UserProfileForm, \
    FinancialLiteracyForm, \
    AutomationForm, LogCategoryForm, PartnerForm, MilestoneYearForm, OutReachForm, ProductProcessForm, ProjectForm, \
    ProductForm, ProvinceForm, DistrictForm, MunicipalitiesForm, \
    Financial_ProgramForm, Automation_PartnersForm, MfsForm, InsuranceForm, Secondary_DataForm, PartnershipForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group, Permission
from .models import UserProfile
from django.shortcuts import get_object_or_404
from django.contrib import messages
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from dashboard.app_setting import MY_SETTING


# Create your views here.


class Dashboard(TemplateView):

    def get(self, request, *args, **kwargs):
        sidebar = LogCategory.objects.all()
        context = {
            "sidebar": sidebar,
            "dashboard": "active",
            "product_count": Product.objects.all().count(),
            "project_count": Project.objects.all().count(),
            "partner_count": Partner.objects.all().count(),
            "user_count": User.objects.all().count()

        }
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # group = Group.objects.get(user=user)
        # log = Log.objects.all().order_by('-id')
        # if group.name == 'admin':
        #     five = FiveW.objects.order_by('id')
        # else:
        #     five = FiveW.objects.select_related('supplier_id').filter(supplier_id=user_data.partner.id)[:10]
        return render(request, 'dashboard.html', context)


class LogCategoryList(LoginRequiredMixin, ListView):
    template_name = 'logcat_list.html'
    model = LogCategory

    def get_context_data(self, **kwargs):
        data = super(LogCategoryList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['logcat'] = 'active'
        query_data = LogCategory.objects.order_by('id')
        data['list'] = query_data

        return data


class LogCategoryUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = LogCategory
    template_name = 'logcat_edit.html'
    form_class = LogCategoryForm
    success_message = 'Log Category Successfully Updated'

    def get_context_data(self, **kwargs):
        data = super(LogCategoryUpdate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['logcat'] = "active"
        return data

    def get_success_url(self):
        return reverse_lazy('logcat-list')


class LogCategoryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogCategory
    template_name = 'logcat_create.html'
    form_class = LogCategoryForm
    success_message = 'LogCategory data created'

    def get_context_data(self, **kwargs):
        data = super(LogCategoryCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['logcat'] = "active"
        # data['active'] = 'program'
        return data

    def get_success_url(self):
        return reverse_lazy('logcat-list')


class FinancialProgramList(LoginRequiredMixin, ListView):
    template_name = 'financial_program_list.html'
    model = FinancialProgram

    def get_context_data(self, **kwargs):
        data = super(FinancialProgramList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['financialliteracy'] = 'active'
        query_data = FinancialProgram.objects.order_by('id')
        data['list'] = query_data
        return data


class MfsList(LoginRequiredMixin, ListView):
    template_name = 'mfs_list.html'
    model = MFS

    def get_context_data(self, **kwargs):
        data = super(MfsList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['mfss'] = 'active'
        query_data = MFS.objects.order_by('id')
        data['list'] = query_data
        return data


class InsuranceList(LoginRequiredMixin, ListView):
    template_name = 'insurance_list.html'
    model = Insurance

    def get_context_data(self, **kwargs):
        data = super(InsuranceList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['insurance'] = 'active'
        query_data = Insurance.objects.order_by('id')
        data['list'] = query_data
        return data


class SecondaryDataList(LoginRequiredMixin, ListView):
    template_name = 'secondary_data_list.html'
    model = SecondaryData

    def get_context_data(self, **kwargs):
        data = super(SecondaryDataList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['secondarydata'] = 'active'
        query_data = SecondaryData.objects.order_by('id')
        data['list'] = query_data
        return data


class LogdataList(LoginRequiredMixin, ListView):
    template_name = 'logdata_list.html'
    model = LogData

    def get_context_data(self, **kwargs):
        data = super(LogdataList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['logdata'] = 'active'
        query_data = LogData.objects.order_by('id')
        data['list'] = query_data
        return data


class AutomationPartnersList(LoginRequiredMixin, ListView):
    template_name = 'automation_partners_list.html'
    model = AutomationPartner

    def get_context_data(self, **kwargs):
        data = super(AutomationPartnersList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['automation_partners'] = 'active'
        query_data = AutomationPartner.objects.order_by('id')
        data['list'] = query_data
        return data


class ProvinceList(LoginRequiredMixin, ListView):
    template_name = 'province_list.html'
    model = Province

    def get_context_data(self, **kwargs):
        data = super(ProvinceList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['province'] = 'active'
        query_data = Province.objects.order_by('id')
        data['list'] = query_data
        return data


class DistrictList(LoginRequiredMixin, ListView):
    template_name = 'district_list.html'
    model = District

    def get_context_data(self, **kwargs):
        data = super(DistrictList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['district'] = 'active'
        query_data = District.objects.order_by('id')
        data['list'] = query_data
        return data


class MunicipalitiesList(LoginRequiredMixin, ListView):
    template_name = 'municipalities_list.html'
    model = Municipality

    def get_context_data(self, **kwargs):
        data = super(MunicipalitiesList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['municipalities'] = 'active'
        query_data = Municipality.objects.order_by('id')
        data['list'] = query_data
        return data


class ProvinceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Province
    template_name = 'province_create.html'
    form_class = ProvinceForm
    success_message = 'Province data created'

    def get_context_data(self, **kwargs):
        data = super(ProvinceCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['province'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('province-list')


class MfsCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = MFS
    template_name = 'mfs_create.html'
    form_class = MfsForm
    success_message = 'Mfs data created'

    def get_context_data(self, **kwargs):
        data = super(MfsCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['municipality'] = Municipality.objects.order_by('id')
        data['partner'] = Partner.objects.order_by('id')
        # data['active'] = 'program'
        data['mfss'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('mfs-list')


class InsuranceCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Insurance
    template_name = 'insurance_create.html'
    form_class = InsuranceForm
    success_message = 'Insurance data created'

    def get_context_data(self, **kwargs):
        data = super(InsuranceCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['partner'] = Partner.objects.order_by('id')
        # data['active'] = 'program'
        data['insurance'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('insurance-list')


class InsuranceEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Insurance
    template_name = 'insurance_edit.html'
    form_class = InsuranceForm
    success_message = 'Insurance data edited'

    def get_context_data(self, **kwargs):
        data = super(InsuranceEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['partner'] = Partner.objects.order_by('id')
        # data['active'] = 'program'
        data['insurance'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('insurance-list')


class SecondaryDataCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SecondaryData
    template_name = 'secondary_data_create.html'
    form_class = Secondary_DataForm
    success_message = 'Secondary Data data created'

    def get_context_data(self, **kwargs):
        data = super(SecondaryDataCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['municipality'] = Municipality.objects.order_by('id')
        # data['active'] = 'program'
        data['secondarydata'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('secondary_data-list')


class SecondaryDataEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SecondaryData
    template_name = 'secondary_data_edit.html'
    form_class = Secondary_DataForm
    success_message = 'Secondary Data data edited'

    def get_context_data(self, **kwargs):
        data = super(SecondaryDataEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['municipality'] = Municipality.objects.order_by('id')
        # data['active'] = 'program'
        data['secondarydata'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('secondary_data-list')


class MfsEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MFS
    template_name = 'mfs_edit.html'
    form_class = MfsForm
    success_message = 'Mfs data edited'

    def get_context_data(self, **kwargs):
        data = super(MfsEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.order_by('id')
        data['districts'] = District.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        data['partners'] = Partner.objects.order_by('id')
        # data['active'] = 'program'
        data['mfss'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('mfs-list')


class ProvinceEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Province
    template_name = 'province_edit.html'
    form_class = ProvinceForm
    success_message = 'Province data edited'

    def get_context_data(self, **kwargs):
        data = super(ProvinceEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['province'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('province-list')


class DistrictCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = District
    template_name = 'district_create.html'
    form_class = DistrictForm
    success_message = 'District data created'

    def get_context_data(self, **kwargs):
        data = super(DistrictCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.order_by('id')
        # data['active'] = 'program'
        data['district'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('district-list')


class DistrictEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = District
    template_name = 'district_edit.html'
    form_class = DistrictForm
    success_message = 'District data edit'

    def get_context_data(self, **kwargs):
        data = super(DistrictEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        # data['active'] = 'program'
        data['district'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('district-list')


class MunicipalitiesCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Municipality
    template_name = 'municipalities_create.html'
    form_class = MunicipalitiesForm
    success_message = 'Municipality data created'

    def get_context_data(self, **kwargs):
        data = super(MunicipalitiesCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        # data['active'] = 'program'
        data['municipalities'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('municipalities-list')


class MunicipalitiesEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Municipality
    template_name = 'municipalities_edit.html'
    form_class = MunicipalitiesForm
    success_message = 'Municipality data edit'

    def get_context_data(self, **kwargs):
        data = super(MunicipalitiesEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        # data['active'] = 'program'
        data['municipalities'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('municipalities-list')


class FinancialProgramCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = FinancialProgram
    template_name = 'financial_program_create.html'
    form_class = Financial_ProgramForm
    success_message = 'Financial Program data created'

    def get_context_data(self, **kwargs):
        data = super(FinancialProgramCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data

        # data['active'] = 'program'
        data['district'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('financial_program-list')


class AutomationPartnersCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = AutomationPartner
    template_name = 'automation_partners_create.html'
    form_class = Automation_PartnersForm
    success_message = 'Automation Partners data created'

    def get_context_data(self, **kwargs):
        data = super(AutomationPartnersCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['partner'] = Partner.objects.order_by('id')
        # data['active'] = 'program'
        data['automation'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('automation_partners-list')


class SakchyamProjectList(LoginRequiredMixin, ListView):
    template_name = 'sakchyamprojects_list.html'
    model = Project

    def get_context_data(self, **kwargs):
        data = super(SakchyamProjectList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['project'] = 'active'
        query_data = Project.objects.order_by('id')
        data['list'] = query_data
        return data


class PartnershipList(LoginRequiredMixin, ListView):
    template_name = 'partnership_list.html'
    model = Partnership
    paginate_by = 2

    def get_context_data(self, **kwargs):
        data = super(PartnershipList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['partnership'] = 'active'
        query_data = Partnership.objects.values('id', 'province_id__name', 'district_id__name', 'municipality_id__name',
                                                'partner_id__name', 'project_id__name', 'branch', 'blb',
                                                'extension_counter', 'tablet', 'other_products', 'beneficiary',
                                                'scf_funds', 'allocated_budget', 'allocated_beneficiary',
                                                'female_percentage', 'total_beneficiary', 'female_beneficiary',
                                                'status', 'start_date', 'end_date', 'project_year',
                                                'leverage').order_by('id')
        paginator = Paginator(query_data, 500)
        page_numbers_range = 1000
        max_index = len(paginator.page_range)
        page_number = self.request.GET.get('page')
        current_page = int(page_number) if page_number else 1
        page_obj = paginator.get_page(page_number)
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        data['page_range'] = page_range

        data['list'] = page_obj
        return data


class PartnershipCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Partnership
    template_name = 'partnership_create.html'
    form_class = PartnershipForm
    success_message = 'Partnership data created'

    def get_context_data(self, **kwargs):
        data = super(PartnershipCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['partner'] = Partner.objects.order_by('id')
        data['project'] = Project.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        # data['active'] = 'program'
        data['partnership'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('partnership-list')


class PartnershipEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Partnership
    template_name = 'partnership_edit.html'
    form_class = PartnershipForm
    success_message = 'Partnership data edited'

    def get_context_data(self, **kwargs):
        data = super(PartnershipEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['province'] = Province.objects.order_by('id')
        data['district'] = District.objects.order_by('id')
        data['partner'] = Partner.objects.order_by('id')
        data['project'] = Project.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        # data['active'] = 'program'
        data['partnership'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('partnership-list')


class PartnershipDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'partnership_delete.html'
    success_message = 'Partnership deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Partnership, id=id)

    def get_success_url(self):
        return reverse_lazy('partnership-list')


class SakchyamProductList(LoginRequiredMixin, ListView):
    template_name = 'sakchyamproducts_list.html'
    model = Product

    def get_context_data(self, **kwargs):
        data = super(SakchyamProductList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['product'] = 'active'
        query_data = Product.objects.order_by('id')
        data['list'] = query_data

        return data


class AutomationList(LoginRequiredMixin, ListView):
    template_name = 'automation_list.html'
    model = Automation
    paginate_by = 2

    def get_context_data(self, **kwargs):
        data = super(AutomationList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['automation'] = 'active'
        query_data = Automation.objects.order_by('id')
        paginator = Paginator(query_data, 500)
        page_numbers_range = 1000
        max_index = len(paginator.page_range)
        page_number = self.request.GET.get('page')
        current_page = int(page_number) if page_number else 1
        page_obj = paginator.get_page(page_number)
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        data['page_range'] = page_range
        data['list'] = page_obj
        return data


class OutReachList(LoginRequiredMixin, ListView):
    template_name = 'outreach_list.html'
    model = Outreach

    def get_context_data(self, **kwargs):
        data = super(OutReachList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['outreach'] = 'active'
        query_data = Outreach.objects.order_by('id')
        data['list'] = query_data
        return data


class FinancialLiteracyList(LoginRequiredMixin, ListView):
    template_name = 'financialliteracy_list.html'
    model = FinancialLiteracy

    def get_context_data(self, **kwargs):
        data = super(FinancialLiteracyList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['financialliteracy'] = 'active'
        query_data = FinancialLiteracy.objects.order_by('id')
        data['list'] = query_data
        return data


class ProductProcessList(LoginRequiredMixin, ListView):
    template_name = 'productprocess_list.html'
    model = ProductProcess

    def get_context_data(self, **kwargs):
        data = super(ProductProcessList, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['productprocess'] = 'active'
        query_data = ProductProcess.objects.order_by('id')
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
        data['partners'] = AutomationPartner.objects.order_by('id')
        data['automation'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('automation-list')


class ProjectCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project_create.html'
    form_class = ProjectForm
    success_message = 'Project data created'

    def get_context_data(self, **kwargs):
        data = super(ProjectCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['project'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-project')


class ProjectEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_edit.html'
    form_class = ProjectForm
    success_message = 'Project data edited'

    def get_context_data(self, **kwargs):
        data = super(ProjectEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['project'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-project')


class ProductCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product_create.html'
    form_class = ProductForm
    success_message = 'product data created'

    def get_context_data(self, **kwargs):
        data = super(ProductCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['product'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-product')


class ProductEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_edit.html'
    form_class = ProductForm
    success_message = 'product data edited'

    def get_context_data(self, **kwargs):
        data = super(ProductEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['product'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-product')


class OutReachCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Outreach
    template_name = 'outreach_create.html'
    form_class = OutReachForm
    success_message = 'Outreach data created'

    def get_context_data(self, **kwargs):
        data = super(OutReachCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['provinces'] = Province.objects.order_by('id')
        data['districts'] = District.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        data['partners'] = Partner.objects.order_by('id')
        data['outreach'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('outreach-list')


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
        data['financialliteracy'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('financialliteracy-list')


class ProductProcessCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ProductProcess
    template_name = 'productprocess_create.html'
    form_class = ProductProcessForm
    success_message = 'ProductProcess data created'

    def get_context_data(self, **kwargs):
        data = super(ProductProcessCreate, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['partner'] = Partner.objects.order_by('id')
        data['product'] = Product.objects.order_by('id')
        data['productprocess'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('productprocess-list')


class ProductProcessEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ProductProcess
    template_name = 'productprocess_edit.html'
    form_class = ProductProcessForm
    success_message = 'ProductProcess data edited'

    def get_context_data(self, **kwargs):
        data = super(ProductProcessEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['partner'] = Partner.objects.order_by('id')
        data['product'] = Product.objects.order_by('id')
        data['productprocess'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('productprocess-list')


class FinancialProgramEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = FinancialProgram
    template_name = 'financial_program_edit.html'
    form_class = Financial_ProgramForm
    success_message = 'Financial Program data '

    def get_context_data(self, **kwargs):
        data = super(FinancialProgramEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data

        # data['active'] = 'program'
        data['district'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('financial_program-list')


class AutomationPartnersEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AutomationPartner
    template_name = 'automation_partners_edit.html'
    form_class = Automation_PartnersForm
    success_message = 'Automation Partners data edited'

    def get_context_data(self, **kwargs):
        data = super(AutomationPartnersEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        # data['active'] = 'program'
        data['partner'] = Partner.objects.order_by('id')
        data['product'] = Product.objects.order_by('id')
        data['automation'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('automation_partners-list')


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
                    code=df['Local Unit Code'][row])
                province = municipality.province_id
                district = municipality.district_id
                partner = AutomationPartner.objects.get(
                    partner__code=df['Partner Code'][row])
                branch = None if df['Name of branch'][row] == '' else df['Name of branch'][row]
                numTablets = 0 if df['No. of Tablet Deployed'][row] == '' else df['No. of Tablet Deployed'][row]
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


def programmeBulkCreate(request):
    template = 'financial_programme_bulk_upload.html'

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
                name = None if df['Programme'][row] == '' else df['Programme'][row]
                code = None if df['Programme Code'][row] == '' else df['Programme Code'][row]
                date = None if df['Date'][row] == '' else df['Date'][row]
                total = None if df['Total Beneficiaries'][row] == '' else df['Total Beneficiaries'][row]
                automation = FinancialProgram.objects.update_or_create(
                    name=name,
                    code=code,
                    date=date,
                    total=total
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Financial Program Bulk Created ")
        return redirect('/dashboard/financial_program-list/', messages)


def mfsBulkCreate(request):
    template = 'mfs_bulk_upload.html'

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
                if df['District Code'][row] != "":
                    district = District.objects.get(
                        n_code=df['District Code'][row])
                else:
                    district = None
                if df['Province Code'][row] != "":
                    province = Province.objects.get(code=df['Province Code'][row])
                else:
                    province = None
                partner = Partner.objects.get(
                    code=df['Partner Code'][row])
                key_innovation = None if df['Key Innovation'][row] == '' else df['Key Innovation'][row]
                achievement_type = None if df['Achievement Type'][row] == '' else df['Achievement Type'][row]
                achieved_number = 0 if df['Achieved Number'][row] == '' else df['Achieved Number'][row]
                mfs = MFS.objects.update_or_create(
                    province_id=province,
                    district_id=district,
                    partner_id=partner,
                    key_innovation=key_innovation,
                    achievement_type=achievement_type,
                    achieved_number=achieved_number
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Mfs Created ")
        return redirect('/dashboard/mfs-list/', messages)


def insuranceBulkCreate(request):
    template = 'insurance_bulk_upload.html'

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
                partner = Partner.objects.get(
                    code=df['Partner Code'][row])
                innovation = None if df['Innovation'][row] == '' else df['Innovation'][row]
                distribution_channel = None if df['Distribution Channel'][row] == '' else df['Distribution Channel'][
                    row]
                product = None if df['Product'][row] == '' else df['Product'][row]
                description = None if df['Description'][row] == '' else df['Description'][row]
                number_of_insurance_sold = 0 if df['Number of Insurance Policies Sold during project period'][
                                                    row] == '' else \
                    df['Number of Insurance Policies Sold during project period'][row]
                amount_of_insurance = 0 if df['Amount of Insurance Premium'][row] == '' else \
                    df['Amount of Insurance Premium'][row]
                amount_of_sum_insuranced = 0 if df['Amount of Sum-Insured'][row] == '' else df['Amount of Sum-Insured'][
                    row]
                amount_of_claim = 0 if df['Amount of Claim'][row] == '' else df['Amount of Claim'][row]
                insurance = Insurance.objects.update_or_create(
                    partner_id=partner,
                    innovation=innovation,
                    distribution_channel=distribution_channel,
                    product=product,
                    description=description,
                    number_of_insurance_sold=number_of_insurance_sold,
                    amount_of_insurance=amount_of_insurance,
                    amount_of_sum_insuranced=amount_of_sum_insuranced,
                    amount_of_claim=amount_of_claim
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Insurance Created ")
        return redirect('/dashboard/insurance-list/', messages)


def productBulkCreate(request):
    template = 'product_bulk_upload.html'

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
                name = None if df['Product Name'][row] == '' else df['Product Name'][row]
                type = None if df['Product Category'][row] == '' else df['Product Category'][row]
                code = None if df['Product Code'][row] == '' else df['Product Code'][row]
                date = None if df['Launch Date'][row] == '' else df['Launch Date'][row]
                product = Product.objects.update_or_create(
                    name=name,
                    type=type,
                    code=code,
                    date=date
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Product Created ")
        return redirect('/dashboard/sakchyam-product/', messages)


def financialliteracyBulkCreate(request):
    template = 'financialliteracy_bulk_upload.html'

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
                partner_id = Partner.objects.get(
                    code=df['Partner Code'][row])
                partner_type = None if df['Partner Type'][row] == '' else df['Partner Type'][row]
                program_id = FinancialProgram.objects.get(
                    code=df['Financial Literacy Initiative Code'][row])
                value = 0 if df['Value'][row] == '' else df['Value'][row]
                single_count = None if df['Total Single Count'][row] == '' else df['Total Single Count'][row]
                financialliteracy = FinancialLiteracy.objects.update_or_create(
                    partner_id=partner_id,
                    partner_type=partner_type,
                    program_id=program_id,
                    value=value,
                    single_count=single_count
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Financial Literacy Created ")
        return redirect('/dashboard/financialliteracy-list/', messages)


def outreachBulkCreate(request):
    template = 'outreach_bulk_upload.html'

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
                    code=df['Local Unit Code'][row])
                province = municipality.province_id
                district = municipality.district_id
                partner = Partner.objects.get(
                    code=df['Partner Code'][row])
                partner_type = None if df['Partner Type'][row] == '' else df['Partner Type'][row]
                market_name = None if df['Market Name'][row] == '' else df['Market Name'][row]
                expansion_driven_by = None if df['Expansion Driven by'][row] == '' else df['Expansion Driven by'][row]
                date_established = None if df['Date established'][row] == '' else df['Date established'][row]
                point_service = None if df['Point of Service'][row] == '' else df['Point of Service'][row]
                g2p_payment = None if df['G2P Payments'][row] == '' else df['G2P Payments'][row]
                gps_point = None if df['GPS Point'][row] == '' else df['GPS Point'][row]
                demonstration_effect = None if df['Demonstration effect'][row] == '' else df['Demonstration effect'][
                    row]

                outreach = Outreach.objects.update_or_create(
                    province_id=province,
                    district_id=district,
                    municipality_id=municipality,
                    partner_id=partner,
                    partner_type=partner_type,
                    market_name=market_name,
                    expansion_driven_by=expansion_driven_by,
                    date_established=date_established,
                    point_service=point_service,
                    g2p_payment=g2p_payment,
                    gps_point=gps_point,
                    demonstration_effect=demonstration_effect

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Outreach Created ")
        return redirect('/dashboard/outreach-list/', messages)


def secondarydataBulkCreate(request):
    template = 'secondary_bulk_upload.html'

    # prompt = {
    #     'order': '''1. Please upload a .csv or .xls file \n
    #                 2. Order of the file columns should be Province, District, Municipality, Partner, Branch, No. of Tablets'''
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
                municipality = Municipality.objects.get(
                    code=df['Local Unit Code'][row])
                province = municipality.province_id
                district = municipality.district_id
                head_quarter = None if df['Head-Quarter of the Local Unit'][row] == '' else \
                    df['Head-Quarter of the Local Unit'][row]
                hdi = None if df['HDI of District'][row] == '' else df['HDI of District'][row]
                population = None if df['Population in the Local Unit'][row] == '' else \
                    df['Population in the Local Unit'][row]
                yearly_fund = None if df['Yearly Central Government Funding'][row] == '' else \
                    df['Yearly Central Government Funding'][row]
                social_security_recipients = None if df['Social Security Payment Recipients'][row] == '' else \
                    df['Social Security Payment Recipients'][row]
                yearly_social_security_payment = None if df['Yearly Social Security Payments'][row] == '' else \
                    df['Yearly Social Security Payments'][row]
                nearest_branch_distance = None if df['Road distance from nearest Commercial Bank Branch (in KM)'][
                                                      row] == '' else \
                    df['Road distance from nearest Commercial Bank Branch (in KM)'][row]
                communication_landline = None if df['Available Means of Communication_Landline'][row] == '' else \
                    df['Available Means of Communication_Landline'][row]
                communication_mobile = None if df['Available Means of Communication_Mobile'][row] == '' else \
                    df['Available Means of Communication_Mobile'][row]
                communication_internet = None if df['Available Means of Communication_Internet'][row] == '' else \
                    df['Available Means of Communication_Internet'][row]
                communication_internet_other = None if df['Available Means of Communication_OtherInternet'][
                                                           row] == '' else \
                    df['Available Means of Communication_OtherInternet'][row]
                available_electricity_maingrid = None if df['Availability of Electricity_MainGrid'][row] == '' else \
                    df['Availability of Electricity_MainGrid'][row]
                available_electricity_micro_hydro = None if df['Availability of Electricity_Micro-Hydro'][
                                                                row] == '' else \
                    df['Availability of Electricity_Micro-Hydro'][row]
                nearest_road_location_name = None if df['Nearest Road Access_LocationName'][row] == '' else \
                    df['Nearest Road Access_LocationName'][row]
                nearest_road_distance = None if df['Nearest Road Access_Distance'][row] == '' else \
                    df['Nearest Road Access_Distance'][row]
                nearest_road_type = None if df['Nearest Road Access_TypeOfRoad'][row] == '' else \
                    df['Nearest Road Access_TypeOfRoad'][row]
                nearest_police_location_name = None if df['Nearest Police Presence_LocationName'][row] == '' else \
                    df['Nearest Police Presence_LocationName'][row]
                nearest_police_distance = None if df['Nearest Police Presence_Distance'][row] == '' else \
                    df['Nearest Police Presence_Distance'][row]
                categorisation_by_sakchyam = None if df['Categorisation by Sakchyam'][row] == '' else \
                    df['Categorisation by Sakchyam'][row]

                outreach = SecondaryData.objects.update_or_create(
                    province_id=province,
                    district_id=district,
                    municipality_id=municipality,
                    hdi=hdi,
                    head_quarter=head_quarter,
                    population=population,
                    yearly_fund=yearly_fund,
                    social_security_recipients=social_security_recipients,
                    yearly_social_security_payment=yearly_social_security_payment,
                    nearest_police_distance=nearest_police_distance,
                    communication_landline=communication_landline,
                    communication_mobile=communication_mobile,
                    communication_internet=communication_internet,
                    communication_internet_other=communication_internet_other,
                    available_electricity_maingrid=available_electricity_maingrid,
                    available_electricity_micro_hydro=available_electricity_micro_hydro,
                    nearest_police_location_name=nearest_police_location_name,
                    nearest_road_location_name=nearest_road_location_name,
                    nearest_road_distance=nearest_road_distance,
                    nearest_road_type=nearest_road_type,
                    categorisation_by_sakchyam=categorisation_by_sakchyam,
                    nearest_branch_distance=nearest_branch_distance

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Secondary Created ")
        return redirect('/dashboard/secondary_data-list/', messages)


def partnershipBulkCreate(request):
    template = 'partnership_bulk_upload.html'

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

        total_range = len(df)
        success_count = 0
        range1 = 0
        range2 = MY_SETTING
        loopcount = 0
        overallloop = 0
        while range1 < total_range:
            for row in range(range1, range2):
                overallloop += 1
                if overallloop <= total_range:
                    try:
                        municipality = Municipality.objects.get(
                            code=df['Local Unit Code'][row])

                        district = municipality.district_id
                        province = municipality.province_id
                        partner = Partner.objects.get(
                            code=df['Partner Code'][row])
                        project = Project.objects.get(
                            code=df['Project Code'][row])
                        branch = None if df['Branch'][row] == '' else df['Branch'][row]
                        blb = None if df['BLB'][row] == '' else df['BLB'][row]
                        extension_counter = None if df['Extension Counter'][row] == '' else df['Extension Counter'][row]
                        tablet = None if df['Tablet'][row] == '' else df['Tablet'][row]
                        other_products = None if df['Other Major Products'][row] == '' else df['Other Major Products'][
                            row]
                        beneficiary = None if df['Beneficiaries'][row] == '' else df['Beneficiaries'][row]
                        scf_funds = None if df['S-CF Funds'][row] == '' else df['S-CF Funds'][row]
                        leverage = None if df['Leverage'][row] == '' else df['Leverage'][row]
                        allocated_budget = None if df['Allocated Funds to Local Units'][row] == '' else \
                            df['Allocated Funds to Local Units'][row]
                        allocated_beneficiary = None if df['Allocated Beneficiaries at Local Units'][row] == '' else \
                            df['Allocated Beneficiaries at Local Units'][row]
                        female_beneficiary = None if df['Female Beneficiaries'][row] == '' else \
                            df['Female Beneficiaries'][row]
                        total_beneficiary = None if df['Total Beneficiaries'][row] == '' else df['Total Beneficiaries'][
                            row]
                        status = None if df['Status'][row] == '' else df['Status'][row]
                        start_date = None if df['Start Date'][row] == '' else df['Start Date'][row]
                        end_date = None if df['End Date'][row] == '' else df['End Date'][row]
                        project_year = None if df['Project Year'][row] == '' else df['Project Year'][row]
                        partnership = Partnership.objects.update_or_create(
                            province_id=province,
                            district_id=district,
                            municipality_id=municipality,
                            partner_id=partner,
                            project_id=project,
                            branch=branch,
                            blb=blb,
                            extension_counter=extension_counter,
                            tablet=tablet,
                            other_products=other_products,
                            beneficiary=beneficiary,
                            scf_funds=scf_funds,
                            leverage=leverage,
                            allocated_budget=allocated_budget,
                            allocated_beneficiary=allocated_beneficiary,
                            female_beneficiary=female_beneficiary,
                            total_beneficiary=total_beneficiary,
                            status=status,
                            start_date=start_date,
                            end_date=end_date,
                            project_year=project_year

                        )
                        loopcount += 1
                        if loopcount == MY_SETTING - 1:
                            range1 += MY_SETTING
                            range2 += MY_SETTING

                        success_count += 1
                    except ObjectDoesNotExist as e:
                        messages.add_message(request, messages.WARNING, str(
                            e) + " for row " + str(row))
                        continue
                if overallloop > total_range:
                    range1 += 1000
            loopcount = 0

        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Partnership Created ")
        return redirect('/dashboard/partnership-list/', messages)


def productprocessBulkCreate(request):
    template = 'productprocess_bulk_upload.html'

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
                partner = Partner.objects.get(
                    code=df['Partner Code'][row])
                product = Product.objects.get(
                    code=df['Product Code'][row])
                partner_type = None if df['Partner Type'][row] == '' else df['Partner Type'][row]
                innovation_area = None if df['Innovation Area'][row] == '' else df['Innovation Area'][row]
                market_failure = None if df['Market Failures'][row] == '' else df['Market Failures'][row]

                productprocess = ProductProcess.objects.update_or_create(

                    partner_id=partner,
                    product_id=product,
                    partner_type=partner_type,
                    innovation_area=innovation_area,
                    market_failure=market_failure

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " ProductProcess Created ")
        return redirect('/dashboard/productprocess-list/', messages)


def MunicipalityBulkCreate(request):
    template = 'municipality_bulk_upload.html'

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
                district = District.objects.get(
                    n_code=df['District Code'][row])
                province = district.province_id
                name = None if df['Name'][row] == '' else df['Name'][row]
                municipality_type = None if df['Municipality Type'][row] == '' else df['Municipality Type'][row]
                hlcit_code = 0 if df['Hlcit Code'][row] == '' else df['Hlcit Code'][row]
                code = 0 if df['Code'][row] == '' else df['Code'][row]

                municipality = Municipality.objects.update_or_create(

                    name=name,
                    code=code,
                    district_id=district,
                    province_id=province,
                    municipality_type=municipality_type,
                    hlcit_code=hlcit_code

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Municipality Created ")
        return redirect('/dashboard/municipalities-list/', messages)


def AutomationPartnerBulkCreate(request):
    template = 'automation_partner_bulk_upload.html'

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
                partner_code = Partner.objects.get(
                    code=df['Partner Code'][row])
                latitude = None if df['Latitude'][row] == '' else df['Latitude'][row]
                date = None if df['Date'][row] == '' else df['Date'][row]
                longitude = None if df['Longitude'][row] == '' else df['Longitude'][row]
                beneficiary = 0 if df['Beneficiaries'][row] == '' else df['Beneficiaries'][row]

                automation_partner = AutomationPartner.objects.update_or_create(
                    partner=partner_code,
                    latitude=latitude,
                    date=date,
                    longitude=longitude,
                    beneficiary=beneficiary

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Automation Partner Created ")
        return redirect('/dashboard/automation_partners-list/', messages)


def DistrictBulkCreate(request):
    template = 'district_bulk_upload.html'

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
                province = Province.objects.get(
                    code=df['Province Code'][row])
                name = None if df['Name'][row] == '' else df['Name'][row]
                code = 0 if df['Code'][row] == '' else df['Code'][row]
                n_code = 0 if df['N Code'][row] == '' else df['N Code'][row]

                district = District.objects.update_or_create(

                    name=name,
                    code=code,
                    province_id=province,
                    n_code=n_code
                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + "District Created ")
        return redirect('/dashboard/district-list/', messages)


def ProvinceBulkCreate(request):
    template = 'province_bulk_upload.html'

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
                name = None if df['Name'][row] == '' else df['Name'][row]
                code = 0 if df['Code'][row] == '' else df['Code'][row]

                province = Province.objects.update_or_create(

                    name=name,
                    code=code,

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Province Created ")
        return redirect('/dashboard/province-list/', messages)


def projectBulkCreate(request):
    template = 'project_bulk_upload.html'

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
                name = None if df['Project Name'][row] == '' else df['Project Name'][row]
                code = 0 if df['Project Code'][row] == '' else df['Project Code'][row]
                investment_primary = None if df['Primary Investment Focus'][row] == '' else \
                    df['Primary Investment Focus'][row]
                investment_secondary = None if df['Secondary Investment Focus'][row] == '' else \
                    df['Secondary Investment Focus'][
                        row]
                leverage = 0 if df['Leverage'][row] == '' else df['Leverage'][row]
                scf_funds = 0 if df['S-CF Funds'][row] == '' else df['S-CF Funds'][row]

                project = Project.objects.update_or_create(

                    name=name,
                    code=code,
                    investment_primary=investment_primary,
                    investment_secondary=investment_secondary,
                    leverage=leverage,
                    scf_funds=scf_funds

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Project Created ")
        return redirect('/dashboard/sakchyam-project/', messages)


def sakchyamPartnerBulkCreate(request):
    template = 'partner_bulk_upload.html'

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

                name = None if df['Partner Institution'][row] == '' else df['Partner Institution'][row]
                code = 0 if df['Partner Code'][row] == '' else df['Partner Code'][row]
                financial_literacy = None if df['Financial Literacy'][row] == '' else df['Financial Literacy'][row]
                partnership = None if df['Partnership'][row] == '' else df['Partnership'][row]
                outreach_expansion = None if df['Outreach Expansion'][row] == '' else df['Outreach Expansion'][row]
                mfs = None if df['MFS'][row] == '' else df['MFS'][row]
                product_process = None if df['ProductProcess'][row] == '' else df['ProductProcess'][row]

                partner = Partner.objects.update_or_create(

                    name=name,
                    code=code,
                    financial_literacy=financial_literacy,
                    partnership=partnership,
                    outreach_expansion=outreach_expansion,
                    mfs=mfs,
                    product_process=product_process

                )
                success_count += 1
            except ObjectDoesNotExist as e:
                messages.add_message(request, messages.WARNING, str(
                    e) + " for row " + str(row))
                continue
        messages.add_message(request, messages.SUCCESS, str(
            success_count) + " Partner Created ")
        return redirect('/dashboard/sakchyam-partners/', messages)


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
        data['partners'] = AutomationPartner.objects.all()
        data['automation'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('automation-list')


class OutReachEdit(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Outreach
    template_name = 'outreach_edit.html'
    form_class = OutReachForm
    success_message = 'OutReach data updated'

    def get_context_data(self, **kwargs):
        data = super(OutReachEdit, self).get_context_data(**kwargs)
        user = self.request.user
        user_data = UserProfile.objects.get(user=user)
        data['user'] = user_data
        data['provinces'] = Province.objects.order_by('id')
        data['districts'] = District.objects.order_by('id')
        data['municipalities'] = Municipality.objects.order_by('id')
        data['partners'] = Partner.objects.all()
        data['automation'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('outreach-list')


def UserEdit(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id=pk)
        user_data = UserProfile.objects.get(user=user)
        context = {
            'user': user,
            'user_data': user_data
        }

        return render(request, 'user_edit.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']
        user = User.objects.get(id=pk)
        userdata = User.objects.filter(id=pk)
        userdata.update(username=username)
        userprofiledata = UserProfile.objects.filter(user=user)
        userprofiledata.update(email=email,full_name=full_name)
        messages.add_message(request, messages.WARNING, "User Updated")
        return redirect('/dashboard/user')


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
        data['automation'] = 'active'
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


class LogCategoryDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'logcat_delete.html'
    success_message = 'LogCategory deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(LogCategory, id=id)

    def get_success_url(self):
        return reverse_lazy('logcat-list')


class MfsDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'mfs_delete.html'
    success_message = 'Mfs deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(MFS, id=id)

    def get_success_url(self):
        return reverse_lazy('mfs-list')


class InsuranceDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'insurance_delete.html'
    success_message = 'Insurance deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Insurance, id=id)

    def get_success_url(self):
        return reverse_lazy('insurance-list')


class SecondaryDataDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'secondary_data_delete.html'
    success_message = 'Secondary Data deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(SecondaryData, id=id)

    def get_success_url(self):
        return reverse_lazy('secondary_data-list')


class FinancialProgramDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'financial_program_delete.html'
    success_message = 'Financial Program deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(FinancialProgram, id=id)

    def get_success_url(self):
        return reverse_lazy('financial_program-list')


class AutomationPartnersDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'automation_partners_delete.html'
    success_message = 'Automation Partners deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(AutomationPartner, id=id)

    def get_success_url(self):
        return reverse_lazy('automation_partners-list')


class DistrictDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'district_delete.html'
    success_message = 'District deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(District, id=id)

    def get_success_url(self):
        return reverse_lazy('district-list')


class ProvinceDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'province_delete.html'
    success_message = 'Province deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Province, id=id)

    def get_success_url(self):
        return reverse_lazy('province-list')


class MunicipalitiesDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'municipalities_delete.html'
    success_message = 'Municipalitiy deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Municipality, id=id)

    def get_success_url(self):
        return reverse_lazy('municipalities-list')


class ProjectDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'project_delete.html'
    success_message = 'Project deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Project, id=id)

    def get_success_url(self):
        return reverse_lazy('sakchyam-project')


class ProductDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    success_message = 'Product deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Product, id=id)

    def get_success_url(self):
        return reverse_lazy('sakchyam-product')


class UserDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'user_delete.html'
    success_message = 'User deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(User, id=id)

    def get_success_url(self):
        return reverse_lazy('user')


class ProductProcessDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'productprocess_delete.html'
    success_message = 'ProductProcess deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(ProductProcess, id=id)

    def get_success_url(self):
        return reverse_lazy('productprocess-list')


class OutReachDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'outreach_delete.html'
    success_message = 'OutReach deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Outreach, id=id)

    def get_success_url(self):
        return reverse_lazy('outreach-list')


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
        data['logcat'] = 'active'
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
        data['logcat'] = 'active'
        query_data = LogSubCategory.objects.filter(
            category__id=self.kwargs['id']).order_by('id')
        data['list'] = query_data
        return data


class LogSubCategoryDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'logsubcategory_delete.html'
    success_message = 'LogSubCategory deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(LogSubCategory, id=id)

    def get_success_url(self):
        return reverse_lazy('logcat-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(LogSubCategoryDelete, self).delete(request, *args, **kwargs)


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
        data['active'] = 'logcat'

        return data

    def get_success_url(self):
        return '/dashboard/logframe-list/' + str(self.kwargs['subcat'])


class LogDataDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'logdata_delete.html'
    success_message = 'LogData deleted'

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(LogData, id=id)

    def get_success_url(self, **kwargs):
        return '/dashboard/logsubcat-list/' + str(self.kwargs['cat'])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(LogDataDelete, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(LogDataDelete, self).get_context_data(**kwargs)
        id = self.kwargs.get('subcat')
        data['id'] = id
        return data


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
        data['active'] = 'logcat'
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
        data['active'] = 'logcat'
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
        data['active'] = 'logcat'
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
        data['userman'] = 'active'
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
        data['userman'] = 'active'
        return data


def signup(request, **kwargs):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            data = UserProfile.objects.create(user=user, full_name=request.POST['full_name'],
                                              email=request.POST['email'],
                                              image=request.FILES['image'])
            user = User.objects.create_user(id=user.id, email=request.POST['email'], username=request.POST['username'],
                                            password=request.POST['password1'])
            user.save()
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
        data['userman'] = 'active'
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
        data['userman'] = 'active'
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


def staff_user(request, **kwargs):
    user = User.objects.get(id=kwargs['id'])
    # user_data = UserProfile.objects.get(user=user)

    if user.is_staff:
        user.is_staff = False
    else:
        user.is_staff = True

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


def usereditrole(request, **kwargs):
    if "GET" == request.method:
        groups = Group.objects.all()
        user = request.user
        user_data = UserProfile.objects.get(user=user)
        return render(request, 'user-edit-role.html', {'user': user_data, 'groups': groups, 'user_id': kwargs['id']})
    else:
        user_id = request.POST['user']
        group_id = request.POST['group_id']
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
        if user.is_superuser:
            messages.info(request, 'Admin cannot be edited')
            return redirect('user')
        else:
            test = user.groups.through.objects.get(user=user_id)
            test.group = group
            test.save()
            messages.info(request, 'Role Edited')
            # notify_message = user.username + ' was assigned ' + group.name + ' role by ' + request.user.username
            # notify = Notification.objects.create(user=user, message=notify_message, type='role',
            #                                      link='/dashboard/user-list')
            return redirect('user')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })


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
        data['partner'] = 'active'
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
        data['partner'] = 'active'
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
        data['partner'] = 'active'
        return data

    def get_success_url(self):
        return reverse_lazy('sakchyam-partners')


class SakchyamPartnersDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
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


def partnerBulkCreate(request):
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
