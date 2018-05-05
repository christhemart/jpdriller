from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('jpdriller/', include('jpdriller.urls')),
    path('admin/', admin.site.urls),
]