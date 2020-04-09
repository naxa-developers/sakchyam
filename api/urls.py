from django.urls import path, include
from api import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('logframe/log-category', views.LogCategoryViewSet.as_view({'get': 'list'}), name='log-category'),
    path('logframe/log-subcategory', views.LogSubCategoryViewSet.as_view({'get': 'list'}), name='log-subcategory'),
    path('logframe/milestone-year', views.MilestoneYearViewSet.as_view({'get': 'list'}), name='milestone-year'),
    path('logframe/log-data', views.LogDataViewSet.as_view({'get': 'list'}), name='log-data'),
    path('logframe/logFrame-data', views.LogDataAlternativeViewSet.as_view({'get': 'list'}), name='logFrame-data'),
    path('logframe/logFrameSingle-data', views.LogDataSingle.as_view({'get': 'list'}), name='logFrameSingle-data'),
    path('token/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/user-permission/', views.UserPermission.as_view({'get': 'list'}), name='user-permission'),
    path('automation/automation-data/', views.AutomationViewSet.as_view({'get': 'list'}), name='automation'),
    path('adminlevel/province/', views.ProvinceViewSet.as_view({'get': 'list'}), name='province'),
    path('adminlevel/district/', views.DistrictViewSet.as_view({'get': 'list'}), name='district'),
    path('adminlevel/municipality/', views.MunicipalityViewSet.as_view({'get': 'list'}), name='municipality'),

]
