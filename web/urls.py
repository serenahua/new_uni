from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('chicken', views.ChickenView.as_view(), name='chicken'),
    path('hotpot', views.HotPotView.as_view(), name='hotpot'),
    path('expense', views.HomeExpenseView.as_view(), name='expense'),
    path('report', views.ReportView.as_view(), name='report'),
    path('system/management', views.SystemManagementView.as_view(), name='system_management'),
    path('system/data', views.SystemDataView.as_view(), name='system_data'),
    path('login', views.LoginView.as_view(), name='login'),
]

