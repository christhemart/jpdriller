from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_vocabulary', views.get_vocabulary, name='get_vocabulary'),
]