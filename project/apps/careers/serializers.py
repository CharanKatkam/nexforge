"""DRF serializers for careers."""

from rest_framework import serializers

from .models import JobApplication, JobOpening


class JobOpeningListSerializer(serializers.ModelSerializer):
    employment_type = serializers.CharField(source="get_employment_type_display")

    class Meta:
        model = JobOpening
        fields = [
            "id", "title", "slug", "department", "location",
            "employment_type", "experience", "posted_at",
        ]


class JobOpeningDetailSerializer(serializers.ModelSerializer):
    employment_type = serializers.CharField(source="get_employment_type_display")

    class Meta:
        model = JobOpening
        fields = [
            "id", "title", "slug", "department", "location", "employment_type",
            "experience", "description", "responsibilities", "requirements",
            "is_open", "posted_at",
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "id", "opening", "name", "email", "phone",
            "resume", "cover_letter", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_opening(self, opening):
        if not opening.is_open:
            raise serializers.ValidationError("This position is no longer open.")
        return opening
