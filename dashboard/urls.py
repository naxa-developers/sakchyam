from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('log-frame-add/<int:cat>/<int:subcat>/<int:title>', views.LogDataCreate.as_view(), name='log-frame-add'),
    path('logtitle-add/<int:subcat>', views.LogTitleCreate.as_view(), name='logtitle-add'),
    path('logframe-list/<int:id>', views.LogFrameList.as_view(), name='logframe-list'),
    path('logsubcat-list/<int:id>', views.LogSubCategoryList.as_view(), name='logsubcat-list'),
    path('logtitle-list/<int:id>', views.LogTitleList.as_view(), name='logtitle-list'),
]
