from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import include, path

#admin.autodiscover()
#admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path('jpdriller/', include('jpdriller.urls')),
    path('admin/', admin.site.urls),
]