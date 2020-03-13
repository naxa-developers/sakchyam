from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Title
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.forms import LogDataForm, TitleForm, LogSubCategoryForm, LogCategoryForm
from django.urls import reverse, reverse_lazy


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            user.is_active = False

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


class FormPage(TemplateView):

    def get(self, request, *args, **kwargs):
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # group = Group.objects.get(user=user)
        # log = Log.objects.all().order_by('-id')
        # if group.name == 'admin':
        #     five = FiveW.objects.order_by('id')
        # else:
        #     five = FiveW.objects.select_related('supplier_id').filter(supplier_id=user_data.partner.id)[:10]
        return render(request, 'log_frame_add.html')


class LogFrameList(LoginRequiredMixin, ListView):
    template_name = 'logframe_list.html'
    model = LogData

    def get_context_data(self, **kwargs):
        data = super(LogFrameList, self).get_context_data(**kwargs)
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        sidebar = LogCategory.objects.order_by('id')
        query_data = LogData.objects.filter(title__id=self.kwargs['id']).order_by('id')
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
        query_data = LogSubCategory.objects.filter(category__id=self.kwargs['id']).order_by('id')
        data['list'] = query_data
        return data


class LogTitleList(LoginRequiredMixin, ListView):
    template_name = 'logtitle_list.html'
    model = LogSubCategory

    def get_context_data(self, **kwargs):
        data = super(LogTitleList, self).get_context_data(**kwargs)
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        sidebar = LogCategory.objects.order_by('id')
        data['sidebar'] = sidebar
        query_data = Title.objects.filter(sub_category__id=self.kwargs['id']).order_by('id')
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
        data['categories'] = LogCategory.objects.filter(id=self.kwargs['cat']).order_by('id')
        data['sub_categories'] = LogSubCategory.objects.filter(id=self.kwargs['subcat']).order_by('id')
        data['titles'] = Title.objects.filter(id=self.kwargs['title']).order_by('id')
        data['years'] = MilestoneYear.objects.order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logframe-list/' + str(self.kwargs['title'])


class LogTitleCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogData
    template_name = 'logtitle_add.html'
    form_class = TitleForm
    success_message = 'Log data successfully Created'

    def get_context_data(self, **kwargs):
        data = super(LogTitleCreate, self).get_context_data(**kwargs)
        user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        # data['active'] = 'program'
        sidebar = LogCategory.objects.all()
        data['sidebar'] = sidebar
        data['sub_categories'] = LogSubCategory.objects.filter(id=self.kwargs['subcat']).order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logtitle-list/' + str(self.kwargs['subcat'])


class LogSubCatCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogData
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
        data['categories'] = LogCategory.objects.filter(id=self.kwargs['cat']).order_by('id')
        data['active'] = 'log_data'
        return data

    def get_success_url(self):
        return '/dashboard/logsubcat-list/' + str(self.kwargs['cat'])
