from django.urls import path, include
from dashboard import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', auth_view.LoginView.as_view(), name='login'),
    path('logout', auth_view.LogoutView.as_view(), name='logout'),
    path('log-frame-add/', views.FormPage.as_view(), name='log-frame-add'),
    path('logframe-list/', views.LogFrameList.as_view(), name='logframe-list'),
]
