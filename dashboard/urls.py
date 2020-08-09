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
    path('outreach-list/', views.OutReachList.as_view(), name='outreach-list'),
    path('productprocess-list/', views.ProductProcessList.as_view(), name='productprocess-list'),
    path('financialliteracy-list/', views.FinancialLiteracyList.as_view(), name='financialliteracy-list'),
    path('automation-add/', views.AutomationCreate.as_view(), name='automation-add'),
    path('productprocess-add/', views.ProductProcessCreate.as_view(), name='productprocess-add'),
    path('outreach-add/', views.OutReachCreate.as_view(), name='outreach-add'),
    path('financialliteracy-add/', views.FinancialLiteracyCreate.as_view(), name='financialliteracy-add'),
    path('automation-bulk-add/', views.automationBulkCreate, name='automation-bulk-add'),
    path('automation-edit/<int:pk>', views.AutomationEdit.as_view(), name='automation-edit'),
    path('outreach-edit/<int:pk>', views.OutReachEdit.as_view(), name='outreach-edit'),
    path('productprocess-edit/<int:pk>', views.ProductProcessEdit.as_view(), name='productprocess-edit'),
    path('automation-delete/<int:pk>', views.AutomationDelete.as_view(), name='automation-delete'),
    path('outreach-delete/<int:pk>', views.OutReachDelete.as_view(), name='outreach-delete'),
    path('productprocess-delete/<int:pk>', views.ProductProcessDelete.as_view(), name='productprocess-delete'),
    path('financialliteracy-delete/<int:pk>', views.FinancialLiteracyDelete.as_view(), name='financialliteracy-delete'),
    path('financialliteracy-edit/<int:pk>', views.FinancialLiteracyEdit.as_view(), name='financialliteracy-edit'),

    #sakchyam partner urls
    path('sakchyam-partners/', views.SakchyamAPartnersList.as_view(), name='sakchyam-partners'),
    path('sakchyam-partners-add/', views.SakchyamAPartnersCreate.as_view(), name='sakchyam-partners-add'),
    path('sakchyam-partners-edit/<int:pk>', views.SakchyamAPartnersEdit.as_view(), name='sakchyam-partners-edit'),
    path('sakchyam-partners-delete/<int:pk>', views.SakchyamAPartnersDelete.as_view(), name='sakchyam-partners-delete'),
    path('sakchyam-partners-bulk-add', views.sakchyamPartnerBulkCreate, name='sakchyam-partners-bulk-add'),

    path('sakchyam-project/', views.SakchyamProjectList.as_view(), name='sakchyam-project'),
    path('project-delete/<int:pk>', views.ProjectDelete.as_view(), name='project-delete'),
    path('sakchyam-product/', views.SakchyamProductList.as_view(), name='sakchyam-product'),
    path('product-delete/<int:pk>', views.ProductDelete.as_view(), name='product-delete'),
    path('project-add/', views.ProjectCreate.as_view(), name='project-add'),
    path('product-add/', views.ProductCreate.as_view(), name='product-add'),
    path('product-edit/<int:pk>', views.ProductEdit.as_view(), name='product-edit'),
    path('project-edit/<int:pk>', views.ProjectEdit.as_view(), name='project-edit'),
    path('province-edit/<int:pk>', views.ProvinceEdit.as_view(), name='province-edit'),
    path('district-edit/<int:pk>', views.DistrictEdit.as_view(), name='district-edit'),
    path('municipalities-edit/<int:pk>', views.MunicipalitiesEdit.as_view(), name='municipalities-edit'),
    path('district-list/', views.DistrictList.as_view(), name='district-list'),
    path('province-list/', views.ProvinceList.as_view(), name='province-list'),
    path('municipalities-list/', views.MunicipalitiesList.as_view(), name='municipalities-list'),
    path('province-add/', views.ProvinceCreate.as_view(), name='province-add'),
    path('district-add/', views.DistrictCreate.as_view(), name='district-add'),
    path('municipalities-add/', views.MunicipalitiesCreate.as_view(), name='municipalities-add'),
    path('milestone-year-add/', views.MilestoneYearCreate.as_view(), name='milestone-year-add'),
    path('district-delete/<int:pk>', views.DistrictDelete.as_view(), name='district-delete'),
    path('province-delete/<int:pk>', views.ProvinceDelete.as_view(), name='province-delete'),
    path('municipalities-delete/<int:pk>', views.MunicipalitiesDelete.as_view(), name='municipalities-delete'),


    path('financial_program-list/', views.Financial_ProgramList.as_view(), name='financial_program-list'),
    path('automation_partners-list/', views.Automation_PartnersList.as_view(), name='automation_partners-list'),

    path('financial_program-delete/<int:pk>', views.Financial_ProgramDelete.as_view(), name='project-delete'),

    path('automation_partners-delete/<int:pk>', views.Automation_PartnersDelete.as_view(), name='project-delete'),

    path('financial_program-edit/<int:pk>', views.Financial_ProgramEdit.as_view(), name='financial_program-edit'),

    path('automation_partners-edit/<int:pk>', views.Automation_PartnersEdit.as_view(), name='automation_partners-edit'),

    path('financial_program-add/', views.Financial_ProgramCreate.as_view(), name='financial_program-add'),

    path('automation_partners-add/', views.Automation_PartnersCreate.as_view(), name='automation_partners-add'),


]
