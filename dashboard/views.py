from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Province, District, Municipality, Automation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.forms import LogDataForm, LogSubCategoryForm, LogCategoryForm, GroupForm, UserProfileForm, \
    AutomationForm, LogCategoryForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group, Permission
from .models import UserProfile


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
        data['active'] = 'automation'
        return data

    def get_success_url(self):
        return reverse_lazy('automation-list')


class LogFrameList(LoginRequiredMixin, ListView):
    template_name = 'logframe_list.html'
    model = LogData

    def get_context_data(self, **kwargs):
        data = super(LogFrameList, self).get_context_data(**kwargs)
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['active'] = 'program'
        sidebar = LogCategory.objects.order_by('id')
        query_data = LogData.objects.filter(sub_category__id=self.kwargs['id']).order_by('id')
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
        data['categories'] = LogCategory.objects.filter(id=self.kwargs['cat']).order_by('id')
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
        data['categories'] = LogCategory.objects.filter(id=self.kwargs['cat']).order_by('id')
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
        data['categories'] = LogCategory.objects.filter(id=self.kwargs['cat']).order_by('id')
        data['sub_categories'] = LogSubCategory.objects.filter(id=self.kwargs['subcat']).order_by('id')
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
