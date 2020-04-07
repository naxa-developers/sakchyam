from django.urls import path, include
from api import views

urlpatterns = [
    path('log-category', views.LogCategoryViewSet.as_view({'get': 'list'}), name='log-category'),
    path('log-subcategory', views.LogSubCategoryViewSet.as_view({'get': 'list'}), name='log-subcategory'),
    path('milestone-year', views.MilestoneYearViewSet.as_view({'get': 'list'}), name='milestone-year'),
    path('log-data', views.LogDataViewSet.as_view({'get': 'list'}), name='log-data'),
    path('logFrame-data', views.LogDataAlternativeViewSet.as_view({'get': 'list'}), name='logFrame-data'),
    path('logFrameSingle-data', views.LogDataSingle.as_view({'get': 'list'}), name='logFrameSingle-data'),

]
