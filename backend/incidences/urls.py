"""Incidence API URL routing."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IncidenceViewSet

router = DefaultRouter()
router.register(r"incidences", IncidenceViewSet, basename="incidence")

urlpatterns = [
    path("", include(router.urls)),
]
