"""Careers API: public job openings + public application submission."""

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import JobApplication, JobOpening
from .serializers import (
    JobApplicationSerializer,
    JobOpeningDetailSerializer,
    JobOpeningListSerializer,
)
from .services import send_application_ack, send_application_notification


class JobOpeningViewSet(ReadOnlyModelViewSet):
    """Public, read-only access to open positions."""

    lookup_field = "slug"
    queryset = JobOpening.objects.filter(is_open=True)
    permission_classes = [AllowAny]
    filterset_fields = ["department", "employment_type"]
    search_fields = ["title", "department", "description"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return JobOpeningDetailSerializer
        return JobOpeningListSerializer


class JobApplicationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Anyone may apply; only staff (HR) may list/update applications."""

    queryset = JobApplication.objects.select_related("opening", "reviewed_by").all()
    serializer_class = JobApplicationSerializer
    throttle_scope = "enquiry"

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_throttles(self):
        if self.action == "create":
            from rest_framework.throttling import ScopedRateThrottle

            return [ScopedRateThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        application = serializer.save(status=JobApplication.Status.NEW)
        send_application_notification(application)
        send_application_ack(application)
