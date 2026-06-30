"""Careers / recruitment models."""

from django.conf import settings
from django.db import models
from django.utils.text import slugify

from apps.core.validators import MaxFileSizeValidator, validate_document_extension


class JobOpening(models.Model):
    """An open position the company is hiring for."""

    class Employment(models.TextChoices):
        FULL_TIME = "full_time", "Full-time"
        PART_TIME = "part_time", "Part-time"
        CONTRACT = "contract", "Contract"
        INTERNSHIP = "internship", "Internship"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    department = models.CharField(max_length=120)
    location = models.CharField(max_length=150)
    employment_type = models.CharField(
        max_length=20, choices=Employment.choices, default=Employment.FULL_TIME
    )
    experience = models.CharField(max_length=80, blank=True)
    description = models.TextField()
    responsibilities = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    is_open = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-posted_at"]
        indexes = [models.Index(fields=["is_open"])]

    def __str__(self) -> str:
        return f"{self.title} ({self.department})"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)


class JobApplication(models.Model):
    """A candidate's application to a job opening."""

    class Status(models.TextChoices):
        NEW = "new", "New"
        SHORTLISTED = "shortlisted", "Shortlisted"
        INTERVIEW = "interview", "Interview"
        HIRED = "hired", "Hired"
        REJECTED = "rejected", "Rejected"

    opening = models.ForeignKey(
        JobOpening, on_delete=models.CASCADE, related_name="applications"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(
        upload_to="resumes/",
        validators=[validate_document_extension, MaxFileSizeValidator(10)],
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_applications",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"])]

    def __str__(self) -> str:
        return f"{self.name} -> {self.opening.title}"
