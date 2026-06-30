"""Careers business logic: email notifications on a new application."""

import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _hr_inbox() -> str:
    return getattr(settings, "HR_INBOX", "") or settings.SALES_INBOX


def send_application_notification(application) -> None:
    """Notify the HR inbox of a new job application. Never raises."""
    try:
        send_mail(
            subject=f"New application: {application.opening.title} — {application.name}",
            message=(
                f"Candidate: {application.name}\n"
                f"Email: {application.email}\nPhone: {application.phone}\n"
                f"Position: {application.opening.title}\n\n"
                f"Cover letter:\n{application.cover_letter}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[_hr_inbox()],
            fail_silently=True,
        )
    except Exception:  # pragma: no cover - defensive
        logger.exception("Failed HR notification for application %s", application.pk)


def send_application_ack(application) -> None:
    """Auto-reply to the candidate confirming receipt. Never raises."""
    try:
        send_mail(
            subject=f"We received your application — {application.opening.title}",
            message=(
                f"Hi {application.name},\n\n"
                f"Thank you for applying for {application.opening.title} at "
                f"NexForge Automation. Our HR team will review your application "
                f"and get back to you if your profile matches.\n\n"
                f"— NexForge Automation HR"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.email],
            fail_silently=True,
        )
    except Exception:  # pragma: no cover - defensive
        logger.exception("Failed applicant ack for application %s", application.pk)
