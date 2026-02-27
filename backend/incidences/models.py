"""Incidence model — the core domain entity."""

import uuid

from django.db import models
from django.utils import timezone


class IncidenceStatus(models.TextChoices):
    UNRESOLVED = "unresolved", "Unresolved"
    RESOLVED = "resolved", "Resolved"
    IGNORED = "ignored", "Ignored"


class Incidence(models.Model):
    """
    Represents a single incidence (error/event group).

    Fields
    ------
    title : str
        Human-readable summary. Indexed with trigram for text search.
    fingerprint : str
        Unique hash identifying the incidence. Indexed for exact-match lookups.
    status : str
        One of ``unresolved``, ``resolved``, ``ignored``.
    first_seen / last_seen : datetime
        Bounding timestamps for the incidence's lifetime.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=512)
    fingerprint = models.CharField(max_length=64, unique=True, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=IncidenceStatus.choices,
        default=IncidenceStatus.UNRESOLVED,
        db_index=True,
    )
    first_seen = models.DateTimeField(default=timezone.now, db_index=True)
    last_seen = models.DateTimeField(default=timezone.now, db_index=True)

    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_seen"]
        indexes = [
            # Composite index for common filter combination
            models.Index(fields=["status", "-last_seen"], name="idx_status_last_seen"),
        ]

    def __str__(self) -> str:
        return f"[{self.status}] {self.title[:80]}"
