"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("incidences.urls")),
    # DRF browsable API auth (login/logout)
    path("api-auth/", include("rest_framework.urls")),
]
