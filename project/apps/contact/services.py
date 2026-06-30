"""Services for contact app - business logic layer."""

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.contact.models import Enquiry


def create_enquiry(name, email, phone, message):
    """Create an enquiry record."""
    return Enquiry.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message,
        status=Enquiry.Status.NEW,
    )


def send_enquiry_email(enquiry):
    """Send HTML email notification for new enquiry."""
    subject = f"New Enquiry: {enquiry.name}"
    html_body = render_to_string("emails/enquiry_notification.html", {"enquiry": enquiry})
    text_body = (
        f"New enquiry received:\n\nName: {enquiry.name}\n"
        f"Email: {enquiry.email}\nPhone: {enquiry.phone}\n"
        f"Message:\n{enquiry.message}"
    )
    try:
        send_mail(
            subject,
            text_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.SALES_INBOX],
            html_message=html_body,
            fail_silently=True,
        )
        return True
    except Exception:
        return False


def send_enquiry_ack(enquiry):
    """Auto-reply to the person who submitted the enquiry. Never raises."""
    try:
        send_mail(
            subject="We received your enquiry — NexForge Automation",
            message=(
                f"Hi {enquiry.name},\n\n"
                f"Thanks for reaching out to NexForge Automation. We have received "
                f"your enquiry and our team will get back to you shortly.\n\n"
                f"Your message:\n{enquiry.message}\n\n"
                f"— NexForge Automation"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[enquiry.email],
            fail_silently=True,
        )
        return True
    except Exception:
        return False


def process_enquiry(name, email, phone, message):
    """Create enquiry and send notification email."""
    enquiry = create_enquiry(name, email, phone, message)
    send_enquiry_email(enquiry)
    send_enquiry_ack(enquiry)
    return enquiry