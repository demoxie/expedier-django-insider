"""
Management command to seed the database with sample incidence data.

Usage:
    python manage.py seed_incidences          # creates 50 incidences
    python manage.py seed_incidences --count 200
    python manage.py seed_incidences --clear   # delete all first
"""

import hashlib
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from incidences.models import Incidence, IncidenceStatus

SAMPLE_TITLES = [
    "TypeError: Cannot read properties of undefined (reading 'map')",
    "ConnectionError: Database connection pool exhausted",
    "TimeoutError: Request to payment gateway timed out after 30s",
    "ValueError: Invalid email format in user registration",
    "PermissionError: User lacks admin privileges for resource",
    "FileNotFoundError: Missing template 'dashboard.html'",
    "IntegrityError: Duplicate key violates unique constraint on email",
    "MemoryError: Worker process exceeded 512MB memory limit",
    "AuthenticationError: JWT token expired for user session",
    "RateLimitError: API rate limit exceeded for client IP",
    "SSLError: Certificate verification failed for upstream service",
    "ParseError: Malformed JSON in request body",
    "NotFoundError: Resource /api/v2/users/999 does not exist",
    "ConfigurationError: Missing required environment variable DB_HOST",
    "SerializationError: Failed to serialize response payload",
    "NetworkError: DNS resolution failed for api.external-service.com",
    "ValidationError: Phone number format not recognized",
    "CacheError: Redis connection refused on port 6379",
    "QueueError: Message broker not available",
    "StorageError: S3 bucket access denied for file upload",
]


class Command(BaseCommand):
    help = "Seed the database with sample Incidence records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of incidences to create (default: 50)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing incidences before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Incidence.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing incidences."))

        count = options["count"]
        statuses = [s.value for s in IncidenceStatus]
        now = timezone.now()
        incidences = []

        for i in range(count):
            title = random.choice(SAMPLE_TITLES)
            # Make fingerprint unique by appending index
            fingerprint = hashlib.sha256(f"{title}-{i}-{now.isoformat()}".encode()).hexdigest()[:40]
            first_seen = now - timedelta(days=random.randint(1, 90), hours=random.randint(0, 23))
            last_seen = first_seen + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

            incidences.append(
                Incidence(
                    title=title,
                    fingerprint=fingerprint,
                    status=random.choice(statuses),
                    first_seen=first_seen,
                    last_seen=min(last_seen, now),
                )
            )

        Incidence.objects.bulk_create(incidences)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} incidences."))
