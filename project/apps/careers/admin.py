"""Admin for careers — HR manages openings and reviews applications."""

from django.contrib import admin

from .models import JobApplication, JobOpening


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "location", "employment_type", "is_open", "posted_at")
    list_filter = ("is_open", "department", "employment_type")
    search_fields = ("title", "department", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_open",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "opening", "email", "status", "reviewed_by", "created_at")
    list_filter = ("status", "opening", "created_at")
    search_fields = ("name", "email", "cover_letter")
    list_editable = ("status",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
