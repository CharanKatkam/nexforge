"""Tests for the careers API."""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from .models import JobApplication, JobOpening


class CareersAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.open_job = JobOpening.objects.create(
            title="Automation Engineer", department="Engineering",
            location="Hyderabad", description="Build PLC systems.", is_open=True,
        )
        cls.closed_job = JobOpening.objects.create(
            title="Old Role", department="Engineering",
            location="Pune", description="Closed.", is_open=False,
        )

    def _resume(self):
        return SimpleUploadedFile("cv.pdf", b"%PDF-1.4 resume", content_type="application/pdf")

    def test_list_shows_only_open(self):
        res = self.client.get("/api/v1/jobs/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)

    def test_detail_by_slug(self):
        res = self.client.get("/api/v1/jobs/automation-engineer/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], "Automation Engineer")

    def test_public_can_apply(self):
        res = self.client.post("/api/v1/applications/", {
            "opening": self.open_job.id, "name": "Asha",
            "email": "asha@example.com", "resume": self._resume(),
        }, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 1)

    def test_cannot_apply_to_closed(self):
        res = self.client.post("/api/v1/applications/", {
            "opening": self.closed_job.id, "name": "Asha",
            "email": "asha@example.com", "resume": self._resume(),
        }, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resume_extension_rejected(self):
        bad = SimpleUploadedFile("malware.exe", b"MZ", content_type="application/x-msdownload")
        res = self.client.post("/api/v1/applications/", {
            "opening": self.open_job.id, "name": "Asha",
            "email": "asha@example.com", "resume": bad,
        }, format="multipart")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anonymous_cannot_list_applications(self):
        res = self.client.get("/api/v1/applications/")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_staff_can_list_applications(self):
        JobApplication.objects.create(
            opening=self.open_job, name="A", email="a@b.com", resume="resumes/x.pdf",
        )
        user = get_user_model().objects.create_user("hr", password="pw-12345-xyz", is_staff=True)
        self.client.force_authenticate(user=user)
        res = self.client.get("/api/v1/applications/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
