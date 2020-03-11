from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from api.models import LogCategory, LogSubCategory, MilestoneYear, LogData, Title
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from dashboard.forms import LogDataForm


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
        query_data = LogData.objects.all()
        # group = Group.objects.get(user=user)
        # if group.name == 'admin':
        #     program_list = Program.objects.order_by('id')
        # else:
        #     program_list = Program.objects.filter(id=user_data.program.id)
        data['list'] = query_data
        # data['user'] = user_data
        # data['active'] = 'program'
        return data


class LogDataCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = LogData
    template_name = 'log_frame_add.html'
    form_class = LogDataForm
    success_message = 'Log data successfully Created'

    def get_context_data(self, **kwargs):
        data = super(LogDataCreate, self).get_context_data(**kwargs)
        # data['open_space'] = OpenSpace.objects.filter(id=self.kwargs['id']).select_related('province',
        #                                                                                    'district',
        #                                                                                    'municipality').order_by(
        #     'id')
        # data['suggest'] = SuggestedUseList.objects.order_by('id')
        # user = self.request.user
        # user_data = UserProfile.objects.get(user=user)
        # data['user'] = user_data
        data['categories'] = LogCategory.objects.all()
        data['sub_categories'] = LogSubCategory.objects.all()
        data['titles'] = Title.objects.all()
        data['years'] = MilestoneYear.objects.all()
        data['active'] = 'log_data'
        return data

