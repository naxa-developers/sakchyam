from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('main/', views.Dashboard.as_view(), name='main'),

    path('log-frame-add/<int:cat>/<int:subcat>/<int:title>', views.LogDataCreate.as_view(), name='log-frame-add'),
    path('logframe-list/<int:id>', views.LogFrameList.as_view(), name='logframe-list'),
    path('logdata-edit/<int:pk>/<int:cat>/<int:subcat>/<int:title>', views.LogDataUpdate.as_view(), name='logdata-edit'),

    path('logsubcat-add/<int:cat>', views.LogSubCatCreate.as_view(), name='logsubcat-add'),
    path('logsubcat-edit/<int:pk>/<int:cat>', views.LogSubCatUpdate.as_view(), name='logsubcat-edit'),
    path('logsubcat-list/<int:id>', views.LogSubCategoryList.as_view(), name='logsubcat-list'),

    path('logtitle-add/<int:subcat>', views.LogTitleCreate.as_view(), name='logtitle-add'),
    path('logtitle-list/<int:id>', views.LogTitleList.as_view(), name='logtitle-list'),
    path('logtitle-edit/<int:pk>/<int:subcat>', views.LogTitleUpdate.as_view(), name='logtitle-edit'),

]
