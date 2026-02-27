"""Unit tests for the Incidence model."""

from django.test import TestCase
from django.utils import timezone

from incidences.models import Incidence, IncidenceStatus


class IncidenceModelTests(TestCase):
    """Verify model creation, defaults, and constraints."""

    def test_create_incidence_with_defaults(self):
        inc = Incidence.objects.create(
            title="Test Error",
            fingerprint="abc123",
        )
        self.assertEqual(inc.status, IncidenceStatus.UNRESOLVED)
        self.assertIsNotNone(inc.id)
        self.assertIsNotNone(inc.first_seen)
        self.assertIsNotNone(inc.last_seen)
        self.assertIsNotNone(inc.created_at)

    def test_str_representation(self):
        inc = Incidence(title="Something broke", status=IncidenceStatus.RESOLVED)
        self.assertEqual(str(inc), "[resolved] Something broke")

    def test_fingerprint_uniqueness(self):
        Incidence.objects.create(title="Error A", fingerprint="unique-fp-1")
        with self.assertRaises(Exception):
            Incidence.objects.create(title="Error B", fingerprint="unique-fp-1")

    def test_status_choices(self):
        valid_statuses = {s.value for s in IncidenceStatus}
        self.assertEqual(valid_statuses, {"unresolved", "resolved", "ignored"})

    def test_ordering_is_by_last_seen_desc(self):
        now = timezone.now()
        old = Incidence.objects.create(
            title="Old", fingerprint="fp-old",
            last_seen=now - timezone.timedelta(days=5),
        )
        new = Incidence.objects.create(
            title="New", fingerprint="fp-new",
            last_seen=now,
        )
        incidences = list(Incidence.objects.all())
        self.assertEqual(incidences[0].pk, new.pk)
        self.assertEqual(incidences[1].pk, old.pk)
