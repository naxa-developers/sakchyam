from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('create-user/', views.signup, name='create-user'),
    # path('add-role/', views.create_role, name='add-role'),
    path('activate/<int:id>', views.activate_user, name='activate'),
    path('main/', views.Dashboard.as_view(), name='main'),
    path('user/', views.UserList.as_view(), name='user'),
    path('role/', views.RoleList.as_view(), name='role'),
    path('add-role/', views.RoleCreate.as_view(), name='add-role'),
    path('edit-role/<int:pk>', views.RoleUpdate.as_view(), name='edit-role'),
    path('assign-role/<int:id>', views.assign_role, name='assign-role'),

    path('log-frame-add/<int:cat>/<int:subcat>', views.LogDataCreate.as_view(), name='log-frame-add'),
    path('logframe-list/<int:id>', views.LogFrameList.as_view(), name='logframe-list'),
    path('logdata-edit/<int:pk>/<int:cat>/<int:subcat>', views.LogDataUpdate.as_view(), name='logdata-edit'),

    path('logsubcat-add/<int:cat>', views.LogSubCatCreate.as_view(), name='logsubcat-add'),
    path('logsubcat-edit/<int:pk>/<int:cat>', views.LogSubCatUpdate.as_view(), name='logsubcat-edit'),
    path('logsubcat-list/<int:id>', views.LogSubCategoryList.as_view(), name='logsubcat-list'),

    # path('logtitle-add/<int:subcat>', views.LogTitleCreate.as_view(), name='logtitle-add'),
    path('logcat-list/', views.LogCategoryList.as_view(), name='logcat-list'),
    path('logcat-add/', views.LogCategoryCreate.as_view(), name='logcat-add'),
    # path('logtitle-edit/<int:pk>/<int:subcat>', views.LogTitleUpdate.as_view(), name='logtitle-edit'),

    path('automation-list/', views.AutomationList.as_view(), name='automation-list'),
    path('automation-add/', views.AutomationCreate.as_view(), name='automation-add'),
    path('automation-bulk-add/', views.automationBulkCreate, name='automation-bulk-add'),
    path('automation-edit/<int:pk>', views.AutomationEdit.as_view(), name='automation-edit'),
    path('automation-delete/<int:pk>', views.AutomationDelete.as_view(), name='automation-delete'),

    #sakchyam partner urls
    path('sakchyam-partners/', views.SakchyamAPartnersList.as_view(), name='sakchyam-partners'),
    path('sakchyam-partners-add/', views.SakchyamAPartnersCreate.as_view(), name='sakchyam-partners-add'),
    path('sakchyam-partners-edit/<int:pk>', views.SakchyamAPartnersEdit.as_view(), name='sakchyam-partners-edit'),
    path('sakchyam-partners-delete/<int:pk>', views.SakchyamAPartnersDelete.as_view(), name='sakchyam-partners-delete'),
    path('sakchyam-partners-bulk-add', views.sakchyamPartnerBulkCreate, name='sakchyam-partners-bulk-add'),
]
