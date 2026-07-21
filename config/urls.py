from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("harit-admin/", admin.site.urls),
    path("", include("directory.urls")),
]
