"""Seed a few sample job openings. Idempotent (get_or_create on title)."""

from django.core.management.base import BaseCommand

from apps.careers.models import JobOpening

OPENINGS = [
    {
        "title": "Senior Automation Engineer", "department": "Engineering",
        "location": "Hyderabad", "employment_type": "full_time",
        "experience": "5+ years",
        "description": "Design and commission PLC/SCADA systems for large manufacturing clients.",
        "responsibilities": "Lead automation projects; program PLCs; commission on site.",
        "requirements": "B.E/B.Tech; Siemens/Allen-Bradley experience; willingness to travel.",
    },
    {
        "title": "IIoT Software Developer", "department": "Software",
        "location": "Pune", "employment_type": "full_time",
        "experience": "3+ years",
        "description": "Build Industrial IoT dashboards and cloud integrations in Python/Django.",
        "responsibilities": "Develop APIs; integrate sensors; build dashboards.",
        "requirements": "Python, Django, REST, MQTT; cloud (AWS/Azure) a plus.",
    },
    {
        "title": "Robotics Integration Intern", "department": "Engineering",
        "location": "Bangalore", "employment_type": "internship",
        "experience": "0-1 years",
        "description": "Assist with robot programming and machine-vision setups.",
        "responsibilities": "Support commissioning; learn ROS and robot SDKs.",
        "requirements": "Final-year/B.E in Mechatronics/EEE; Python basics.",
    },
]


class Command(BaseCommand):
    help = "Load sample job openings for the careers page."

    def handle(self, *args, **options):
        for o in OPENINGS:
            JobOpening.objects.get_or_create(title=o["title"], defaults=o)
        self.stdout.write(self.style.SUCCESS(f"Careers seed complete ({JobOpening.objects.count()} openings)."))
