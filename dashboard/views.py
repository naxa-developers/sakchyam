from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


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

