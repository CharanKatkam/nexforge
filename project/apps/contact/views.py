"""Enquiry API: public create + staff-only CRM list/update."""

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Enquiry
from .serializers import EnquirySerializer
from .services import send_enquiry_ack, send_enquiry_email


class EnquiryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Anyone may submit an enquiry; only staff may list/update them."""

    serializer_class = EnquirySerializer
    throttle_scope = "enquiry"

    def get_queryset(self):
        user = self.request.user
        # swagger_fake_view: schema generation runs with an anonymous request.
        if getattr(self, "swagger_fake_view", False) or not user.is_authenticated:
            return Enquiry.objects.none()
        if user.is_staff:
            return Enquiry.objects.select_related("assigned_to").all()
        return Enquiry.objects.filter(assigned_to=user)

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_throttles(self):
        # Tight throttle only on the public create path.
        if self.action == "create":
            from rest_framework.throttling import ScopedRateThrottle

            return [ScopedRateThrottle()]
        return super().get_throttles()

    def perform_create(self, serializer):
        enquiry = serializer.save(status=Enquiry.Status.NEW, assigned_to=None)
        send_enquiry_email(enquiry)   # notify sales
        send_enquiry_ack(enquiry)     # auto-reply to the submitter
