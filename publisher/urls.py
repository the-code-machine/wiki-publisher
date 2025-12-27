# publisher/urls.py
from django.urls import path
from . import views  # Import views from the current folder

urlpatterns = [
    # path(URL_pattern, view_function, name_reference)
    path('', views.home, name='home'),
    path('get-started/', views.get_started, name='get_started'),


    # New Dashboard URLs
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('dashboard/upload/', views.upload_files, name='upload_files'),

    path('api/fetch-repo/', views.fetch_repo, name='fetch_repo'),
    path('dashboard/mapping/', views.mapping_config, name='mapping_config'),
    path('dashboard/publish/', views.publish, name='publish'),
    path('dashboard/log/', views.publish_log, name='publish_log'),
    path('dashboard/settings/', views.settings, name='settings'),
]