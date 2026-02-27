"""Tests for the IncidenceFilter — verifies each query parameter."""

from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from incidences.filters import IncidenceFilter
from incidences.models import Incidence, IncidenceStatus


class IncidenceFilterTests(TestCase):
    """Test all seven filter parameters individually and combined."""

    @classmethod
    def setUpTestData(cls):
        now = timezone.now()
        cls.now = now

        cls.inc_a = Incidence.objects.create(
            title="TypeError in payment module",
            fingerprint="fp-payment-001",
            status=IncidenceStatus.UNRESOLVED,
            first_seen=now - timedelta(days=10),
            last_seen=now - timedelta(days=1),
        )
        cls.inc_b = Incidence.objects.create(
            title="Connection timeout on dashboard",
            fingerprint="fp-dashboard-002",
            status=IncidenceStatus.RESOLVED,
            first_seen=now - timedelta(days=5),
            last_seen=now,
        )
        cls.inc_c = Incidence.objects.create(
            title="TypeError in auth service",
            fingerprint="fp-auth-003",
            status=IncidenceStatus.IGNORED,
            first_seen=now - timedelta(days=30),
            last_seen=now - timedelta(days=20),
        )

    # --- Text search (q) ---
    def test_filter_by_q_case_insensitive(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"q": "typeerror"}, queryset=qs)
        self.assertEqual(f.qs.count(), 2)  # inc_a and inc_c

    def test_filter_by_q_partial_match(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"q": "payment"}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().pk, self.inc_a.pk)

    def test_filter_by_q_no_results(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"q": "nonexistent-term"}, queryset=qs)
        self.assertEqual(f.qs.count(), 0)

    # --- Fingerprint ---
    def test_filter_by_fingerprint_exact(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"fingerprint": "fp-dashboard-002"}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().pk, self.inc_b.pk)

    def test_filter_by_fingerprint_no_partial(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"fingerprint": "fp-dashboard"}, queryset=qs)
        self.assertEqual(f.qs.count(), 0)

    # --- Status ---
    def test_filter_by_status(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"status": "resolved"}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().pk, self.inc_b.pk)

    # --- first_seen range ---
    def test_filter_by_first_seen_from(self):
        qs = Incidence.objects.all()
        cutoff = (self.now - timedelta(days=7)).isoformat()
        f = IncidenceFilter({"first_seen_from": cutoff}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().pk, self.inc_b.pk)

    def test_filter_by_first_seen_to(self):
        qs = Incidence.objects.all()
        cutoff = (self.now - timedelta(days=7)).isoformat()
        f = IncidenceFilter({"first_seen_to": cutoff}, queryset=qs)
        self.assertEqual(f.qs.count(), 2)  # inc_a (10 days ago) and inc_c (30 days ago)

    # --- last_seen range ---
    def test_filter_by_last_seen_from(self):
        qs = Incidence.objects.all()
        cutoff = (self.now - timedelta(days=2)).isoformat()
        f = IncidenceFilter({"last_seen_from": cutoff}, queryset=qs)
        self.assertEqual(f.qs.count(), 2)  # inc_a and inc_b

    def test_filter_by_last_seen_to(self):
        qs = Incidence.objects.all()
        cutoff = (self.now - timedelta(days=15)).isoformat()
        f = IncidenceFilter({"last_seen_to": cutoff}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)  # inc_c (20 days ago)

    # --- Combined filters ---
    def test_combined_q_and_status(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({"q": "TypeError", "status": "unresolved"}, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().pk, self.inc_a.pk)

    def test_combined_status_and_date_range(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({
            "status": "unresolved",
            "first_seen_from": (self.now - timedelta(days=15)).isoformat(),
            "first_seen_to": (self.now - timedelta(days=5)).isoformat(),
        }, queryset=qs)
        self.assertEqual(f.qs.count(), 1)
        self.assertEqual(f.qs.first().pk, self.inc_a.pk)

    def test_no_filters_returns_all(self):
        qs = Incidence.objects.all()
        f = IncidenceFilter({}, queryset=qs)
        self.assertEqual(f.qs.count(), 3)
