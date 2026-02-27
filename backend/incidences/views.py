"""
Incidence API views.

Provides a read-only list/retrieve endpoint for staff users with full
filtering, ordering, and pagination support.
"""

import logging
import time

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .filters import IncidenceFilter
from .models import Incidence
from .serializers import IncidenceSerializer

logger = logging.getLogger(__name__)


class IncidenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving incidences.

    **Permissions**: Staff users only (``IsAdminUser``).

    **Filtering**: All seven query parameters are supported — see ``IncidenceFilter``.

    **Ordering**: Supports ordering by ``first_seen``, ``last_seen``, ``status``, ``title``.
    Default order is ``-last_seen`` (most recent first).

    **Pagination**: ``PageNumberPagination`` with 25 results per page.
    """

    queryset = Incidence.objects.all()
    serializer_class = IncidenceSerializer
    filterset_class = IncidenceFilter
    ordering_fields = ["first_seen", "last_seen", "status", "title"]
    ordering = ["-last_seen"]

    def list(self, request, *args, **kwargs):
        start = time.monotonic()
        response = super().list(request, *args, **kwargs)
        elapsed_ms = (time.monotonic() - start) * 1000

        # Structured log for observability
        logger.info(
            "incidence_search",
            extra={
                "query_params": dict(request.query_params),
                "result_count": response.data.get("count", 0) if isinstance(response.data, dict) else len(response.data),
                "elapsed_ms": round(elapsed_ms, 2),
                "user_id": request.user.pk,
            },
        )
        return response
