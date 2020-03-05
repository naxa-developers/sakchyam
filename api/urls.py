from django.urls import path, include
from api import views


urlpatterns = [
    path('log_category', views.LogCategoryViewSet.as_view({'get': 'list'}), name='log_category_list'),
    path('log_sub_category', views.LogSubCategoryViewSet.as_view({'get': 'list'}), name='log_sub_category_list'),
    path('milestone_year', views.MilestoneYearViewSet.as_view({'get': 'list'}), name='milestone_year'),
    path('log_data', views.LogDataViewSet.as_view({'get': 'list'}), name='log_data_list'),
    path('log_data_alt', views.LogDataAlternativeViewSet.as_view({'get': 'list'}), name='log_data_list'),

    # #user related urls
    # path('signup', views.signup, name='signup'),


]
