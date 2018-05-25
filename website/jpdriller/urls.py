from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('check_username', views.check_username, name='check_username'),
    path('get_vocabulary', views.get_vocabulary, name='get_vocabulary'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('stat_update', views.stat_update, name='stat_update'),
    path('save_settings', views.save_settings, name='save_settings'),
    path('save_groups', views.save_groups, name='save_groups'),
]