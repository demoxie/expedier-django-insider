"""
django-filter FilterSet for the Incidence list endpoint.

Supports all seven query parameters from the spec:
    q              → case-insensitive icontains on title
    fingerprint    → exact match
    status         → exact match (validated via ChoiceFilter)
    first_seen_from / first_seen_to  → inclusive date range
    last_seen_from  / last_seen_to   → inclusive date range
"""

import logging

from django_filters import rest_framework as filters

from .models import Incidence, IncidenceStatus

logger = logging.getLogger(__name__)


class IncidenceFilter(filters.FilterSet):
    q = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Search title (case-insensitive)",
    )
    fingerprint = filters.CharFilter(
        field_name="fingerprint",
        lookup_expr="exact",
        label="Exact fingerprint match",
    )
    status = filters.ChoiceFilter(
        field_name="status",
        choices=IncidenceStatus.choices,
        label="Incidence status",
    )

    # Date-range filters — ISO 8601 input expected
    first_seen_from = filters.IsoDateTimeFilter(
        field_name="first_seen",
        lookup_expr="gte",
        label="First seen after (inclusive)",
    )
    first_seen_to = filters.IsoDateTimeFilter(
        field_name="first_seen",
        lookup_expr="lte",
        label="First seen before (inclusive)",
    )
    last_seen_from = filters.IsoDateTimeFilter(
        field_name="last_seen",
        lookup_expr="gte",
        label="Last seen after (inclusive)",
    )
    last_seen_to = filters.IsoDateTimeFilter(
        field_name="last_seen",
        lookup_expr="lte",
        label="Last seen before (inclusive)",
    )

    class Meta:
        model = Incidence
        fields = [
            "q",
            "fingerprint",
            "status",
            "first_seen_from",
            "first_seen_to",
            "last_seen_from",
            "last_seen_to",
        ]
