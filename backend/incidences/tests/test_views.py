"""API integration tests for the Incidence viewset."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from incidences.models import Incidence, IncidenceStatus


class IncidenceAPITestCase(TestCase):
    """Base test case with common setup for API tests."""

    @classmethod
    def setUpTestData(cls):
        cls.staff_user = User.objects.create_user(
            username="staffuser", password="testpass123", is_staff=True,
        )
        cls.regular_user = User.objects.create_user(
            username="regularuser", password="testpass123", is_staff=False,
        )
        now = timezone.now()
        cls.now = now

        cls.inc1 = Incidence.objects.create(
            title="TypeError in payment module",
            fingerprint="fp-001",
            status=IncidenceStatus.UNRESOLVED,
            first_seen=now - timedelta(days=10),
            last_seen=now - timedelta(days=1),
        )
        cls.inc2 = Incidence.objects.create(
            title="Connection timeout on dashboard",
            fingerprint="fp-002",
            status=IncidenceStatus.RESOLVED,
            first_seen=now - timedelta(days=5),
            last_seen=now,
        )
        cls.inc3 = Incidence.objects.create(
            title="Memory leak in worker",
            fingerprint="fp-003",
            status=IncidenceStatus.IGNORED,
            first_seen=now - timedelta(days=30),
            last_seen=now - timedelta(days=20),
        )

    def setUp(self):
        self.client = APIClient()


class PermissionTests(IncidenceAPITestCase):
    """Verify staff-only access control."""

    def test_unauthenticated_user_gets_403(self):
        response = self.client.get("/api/incidences/")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_non_staff_user_gets_403(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/api/incidences/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_gets_200(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get("/api/incidences/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListEndpointTests(IncidenceAPITestCase):
    """Test the list endpoint with pagination and filtering."""

    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.staff_user)

    def test_list_returns_paginated_results(self):
        response = self.client.get("/api/incidences/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 3)

    def test_filter_by_q(self):
        response = self.client.get("/api/incidences/", {"q": "TypeError"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["fingerprint"], "fp-001")

    def test_filter_by_fingerprint(self):
        response = self.client.get("/api/incidences/", {"fingerprint": "fp-002"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Connection timeout on dashboard")

    def test_filter_by_status(self):
        response = self.client.get("/api/incidences/", {"status": "ignored"})
        self.assertEqual(response.data["count"], 1)

    def test_filter_by_first_seen_range(self):
        cutoff_from = (self.now - timedelta(days=7)).isoformat()
        cutoff_to = (self.now - timedelta(days=3)).isoformat()
        response = self.client.get("/api/incidences/", {
            "first_seen_from": cutoff_from,
            "first_seen_to": cutoff_to,
        })
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["fingerprint"], "fp-002")

    def test_filter_by_last_seen_range(self):
        cutoff = (self.now - timedelta(days=2)).isoformat()
        response = self.client.get("/api/incidences/", {"last_seen_from": cutoff})
        self.assertEqual(response.data["count"], 2)  # inc1 and inc2

    def test_combined_filters(self):
        response = self.client.get("/api/incidences/", {
            "q": "TypeError",
            "status": "unresolved",
        })
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["fingerprint"], "fp-001")

    def test_empty_results(self):
        response = self.client.get("/api/incidences/", {"q": "nonexistent-xyz"})
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_ordering_default_is_last_seen_desc(self):
        response = self.client.get("/api/incidences/")
        results = response.data["results"]
        self.assertEqual(results[0]["fingerprint"], "fp-002")  # most recent last_seen

    def test_retrieve_single_incidence(self):
        response = self.client.get(f"/api/incidences/{self.inc1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["fingerprint"], "fp-001")
        self.assertIn("status_display", response.data)

    def test_response_fields(self):
        response = self.client.get(f"/api/incidences/{self.inc1.pk}/")
        expected_fields = {
            "id", "title", "fingerprint", "status", "status_display",
            "first_seen", "last_seen", "created_at", "updated_at",
        }
        self.assertEqual(set(response.data.keys()), expected_fields)

    def test_write_methods_not_allowed(self):
        """Viewset is read-only; POST/PUT/DELETE should be rejected."""
        response = self.client.post("/api/incidences/", {"title": "new"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(f"/api/incidences/{self.inc1.pk}/", {"title": "updated"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(f"/api/incidences/{self.inc1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
