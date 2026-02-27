"""Admin configuration for the Incidence model."""

from django.contrib import admin

from .models import Incidence


@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    list_display = ["title", "fingerprint", "status", "first_seen", "last_seen"]
    list_filter = ["status", "first_seen", "last_seen"]
    search_fields = ["title", "fingerprint"]
    readonly_fields = ["id", "created_at", "updated_at"]
