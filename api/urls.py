from django.urls import path, include
from api.views import LogCategoryViewSet, LogSubCategoryViewSet, LogDataViewSet, MilestoneYearViewSet, \
    LogDataAlternativeViewSet

urlpatterns = [
    path('log_category', LogCategoryViewSet.as_view({'get': 'list'}), name='log_category_list'),
    path('log_sub_category', LogSubCategoryViewSet.as_view({'get': 'list'}), name='log_sub_category_list'),
    path('milestone_year', MilestoneYearViewSet.as_view({'get': 'list'}), name='milestone_year'),
    path('log_data', LogDataViewSet.as_view({'get': 'list'}), name='log_data_list'),
    path('log_data_alt', LogDataAlternativeViewSet.as_view({'get': 'list'}), name='log_data_list'),
]
