from django.conf.urls import include, url
from django.contrib import admin
from directions import views

urlpatterns = [
    url(r'^directions/', include('directions.urls')),
    url(r'^admin/', admin.site.urls),
    ]
