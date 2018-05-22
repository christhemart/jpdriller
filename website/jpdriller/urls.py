from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('get_vocabulary', views.get_vocabulary, name='get_vocabulary'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('stat_update', views.stat_update, name='stat_update'),
]