from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.forms import LogDataForm, LogSubCategoryForm, LogCategoryForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group, Permission
from .models import UserProfile


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


# class LogTitleList(LoginRequiredMixin, ListView):
#     template_name = 'logtitle_list.html'
#     model = LogSubCategory
#
#     def get_context_data(self, **kwargs):
#         data = super(LogTitleList, self).get_context_data(**kwargs)
#         # user = self.request.user
#         # user_data = UserProfile.objects.get(user=user)
#         # data['active'] = 'program'
#         sidebar = LogCategory.objects.order_by('id')
#         data['sidebar'] = sidebar
#         query_data = Title.objects.filter(sub_category__id=self.kwargs['id']).order_by('id')
#         data['list'] = query_data
#         return data


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


# class LogTitleCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
#     model = Title
#     template_name = 'logtitle_add.html'
#     form_class = TitleForm
#     success_message = 'Log data successfully Created'
#
#     def get_context_data(self, **kwargs):
#         data = super(LogTitleCreate, self).get_context_data(**kwargs)
#         user = self.request.user
#         # user_data = UserProfile.objects.get(user=user)
#         # data['user'] = user_data
#         # data['active'] = 'program'
#         sidebar = LogCategory.objects.all()
#         data['sidebar'] = sidebar
#         data['sub_categories'] = LogSubCategory.objects.filter(id=self.kwargs['subcat']).order_by('id')
#         data['active'] = 'log_data'
#         return data
#
#     def get_success_url(self):
#         return '/dashboard/logtitle-list/' + str(self.kwargs['subcat'])


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


# class LogTitleUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
#     model = Title
#     template_name = 'logtitle_edit.html'
#     form_class = TitleForm
#     success_message = 'Log data successfully Created'
#
#     def get_context_data(self, **kwargs):
#         data = super(LogTitleUpdate, self).get_context_data(**kwargs)
#         user = self.request.user
#         # user_data = UserProfile.objects.get(user=user)
#         # data['user'] = user_data
#         # data['active'] = 'program'
#         sidebar = LogCategory.objects.all()
#         data['sidebar'] = sidebar
#         data['sub_categories'] = LogSubCategory.objects.filter(id=self.kwargs['subcat']).order_by('id')
#         data['active'] = 'log_data'
#         return data
#
#     def get_success_url(self):
#         return '/dashboard/logtitle-list/' + str(self.kwargs['subcat'])


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
            if kwargs['group'] != 0:
                group = Group.objects.get(pk=kwargs['group'])
                user.groups.add(group)

            UserProfile.objects.create(user=user, name=request.POST['name'], email=request.POST['email'],
                                       partner_id=int(request.POST['partner']), image=request.FILES['image'])

            # notify_message = request.POST['email'] + ' has created account by username ' + request.POST['username']
            #
            # notify_messages = 'Activate account for user ' + request.POST['username']
            #
            # notify = Notification.objects.create(user=user, message=notify_message, type='signup',
            #                                      link='/dashboard/user-list')
            # notified = Notification.objects.create(user=user, message=notify_messages, type='signup',
            #                                        link='/dashboard/user-list')
            return render(request, 'registered_message.html', {'user': request.POST['name']})
        # else:
        #     if kwargs['group'] == 0:
        #         partner = Partner.objects.all()
        #         # program = Program.objects.all()
        #         # project = Project.objects.all()
        #     else:
        #         partner = Partner.objects.filter(id=kwargs['partner'])
        #         # program = Program.objects.filter(id=kwargs['program'])
        #         # project = Project.objects.filter(id=kwargs['project'])
        #
        #     return render(request, 'signups.html',
        #                   {'form': form, 'partners': partner, })

    else:
        form = UserCreationForm()
        # if kwargs['group'] == 0:
        #     partner = Partner.objects.all()
        #     # program = Program.objects.all()
        #     # project = Project.objects.all()
        # else:
        #     partner = Partner.objects.filter(id=kwargs['partner'])
        #     # program = Program.objects.filter(id=kwargs['program'])
        #     # project = Project.objects.filter(id=kwargs['project'])

        return render(request, 'signups.html',
                      {'form': form, 'partners': partner, })


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


def activate_user(request, **kwargs):
    user = User.objects.get(id=kwargs['id'])
    # user_data = UserProfile.objects.get(user=user)

    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True

    user.save()
    return redirect('user')
