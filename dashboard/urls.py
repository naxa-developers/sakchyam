from django.urls import path, include
from dashboard import views


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('log-frame-add/', views.LogDataCreate.as_view(), name='log-frame-add'),
    path('logframe-list/', views.LogFrameList.as_view(), name='logframe-list'),
]
