"""Template (server-rendered) page views."""

from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.core.paginator import Paginator

from apps.blog.models import BlogPost
from apps.content.models import Award, Download, FAQ, GalleryItem, Testimonial
from apps.core.models import Client, Industry, Technology
from apps.projects.models import Project
from apps.services.models import Service

# Selectors
from apps.core.selectors import (
    get_featured_projects,
    get_active_services,
    get_active_testimonials,
    get_published_blog_posts,
    get_active_faqs,
    get_all_gallery_items,
    get_all_awards,
    get_all_downloads,
    get_all_industries,
)
from apps.projects.selectors import get_project_detail, get_related_projects
from apps.services.selectors import get_service_detail, get_active_services as get_services_list
from apps.blog.selectors import get_post_detail, get_published_posts, get_all_categories
from apps.content.selectors import (
    get_faqs_by_category,
    get_active_testimonials as get_content_testimonials,
)


def home(request):
    """Landing page: featured projects, active services, testimonials, stats, industries, process."""
    stats = {
        "employees": "145+",
        "projects": "650+",
        "clients": "300+",
        "cities": "42",
        "industries": "12",
        "satisfaction": "98%",
        "efficiency": "18%",
        "downtime": "35%",
    }
    industries = Industry.objects.all().order_by("name")[:8]
    process_steps = [
        {"number": "01", "title": "Discover", "desc": "We analyze your factory operations and identify automation opportunities."},
        {"number": "02", "title": "Design", "desc": "Custom engineering solutions tailored to your production requirements."},
        {"number": "03", "title": "Deploy", "desc": "Implementation, testing, and commissioning with minimal downtime."},
        {"number": "04", "title": "Optimize", "desc": "Ongoing support, predictive maintenance, and continuous improvement."},
    ]
    clients_with_logos = Client.objects.exclude(logo="").order_by("name")
    ctx = {
        "featured": get_featured_projects(6),
        "services": get_active_services(6),
        "testimonials": get_active_testimonials(6),
        "stats": stats,
        "industries": industries,
        "process_steps": process_steps,
        "client_logos": clients_with_logos,
    }
    return render(request, "core/home.html", ctx)


def about(request):
    """About page with vision, mission, values, stats, and awards."""
    stats = {
        "employees": "145+",
        "projects": "650+",
        "clients": "300+",
        "cities": "42",
        "industries": "12",
        "satisfaction": "98%",
    }
    values = [
        "Innovation", "Engineering Excellence", "Integrity", "Customer Success",
        "Operational Excellence", "Continuous Improvement", "Industrial Safety",
        "Sustainability", "Quality Without Compromise", "Respect for People",
    ]
    why_choose = [
        "145+ Automation Professionals",
        "650+ Successfully Delivered Projects",
        "300+ Manufacturing Clients",
        "Presence Across India",
        "24×7 Technical Support",
        "Industry 4.0 Specialists",
        "AI Enabled Manufacturing Solutions",
        "ISO 9001 Quality Processes",
        "Dedicated Project Managers",
        "Certified Automation Engineers",
        "End-to-End Engineering Services",
        "Turnkey Project Execution",
    ]
    ctx = {
        "awards": Award.objects.all(),
        "stats": stats,
        "values": values,
        "why_choose": why_choose,
    }
    return render(request, "core/about.html", ctx)


def privacy(request):
    return render(request, "core/privacy.html")


def terms(request):
    return render(request, "core/terms.html")


# --- Projects -------------------------------------------------------------
def projects_portfolio(request):
    """Portfolio page with filter/search populated client-side via API."""
    return render(
        request,
        "projects/portfolio.html",
        {
            "industries": get_all_industries(),
            "technologies": Technology.objects.all().order_by("name"),
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.select_related("industry", "client").prefetch_related(
            "technologies", "gallery", "videos", "deliverables",
            "milestones", "before_after",
        ),
        slug=slug,
    )
    related = get_related_projects(project, 3)
    return render(request, "projects/detail.html", {"project": project, "related": related})


# --- Services -------------------------------------------------------------
def services_list(request):
    services_qs = get_services_list()
    paginator = Paginator(services_qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "services/list.html", {"page_obj": page_obj})


def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects.prefetch_related(
            "technologies", "industries", "benefits", "deliverables"
        ),
        slug=slug,
        is_active=True,
    )
    # Per-service CTAs from content pack (url_name for {% url %} resolution)
    service_ctas = {
        "plc-programming-industrial-control-systems": [
            ("Request Technical Proposal", "contact", "btn-brand"),
            ("Book Site Visit", "contact", "btn-outline-brand"),
            ("Talk to Engineer", "contact", "btn-outline-secondary"),
            ("Download Brochure", "downloads", "btn-outline-secondary"),
        ],
        "scada-development": [
            ("Schedule Demo", "contact", "btn-brand"),
            ("Request Consultation", "contact", "btn-outline-brand"),
            ("Download Case Study", "downloads", "btn-outline-secondary"),
        ],
        "industrial-iot-solutions": [
            ("Get Free Consultation", "contact", "btn-brand"),
            ("Talk to Expert", "contact", "btn-outline-brand"),
            ("Book Factory Audit", "contact", "btn-outline-secondary"),
        ],
        "robotics-integration": [
            ("Request Proposal", "contact", "btn-brand"),
            ("Schedule Demo", "contact", "btn-outline-brand"),
        ],
        "machine-vision-inspection": [
            ("Request Consultation", "contact", "btn-brand"),
            ("Book Demo", "contact", "btn-outline-brand"),
        ],
        "predictive-maintenance": [
            ("Get Free Consultation", "contact", "btn-brand"),
            ("Talk to Expert", "contact", "btn-outline-brand"),
        ],
        "electrical-control-panel-manufacturing": [
            ("Request Quote", "contact", "btn-brand"),
            ("Technical Discussion", "contact", "btn-outline-brand"),
        ],
        "energy-monitoring-solutions": [
            ("Request Audit", "contact", "btn-brand"),
            ("Download Brochure", "downloads", "btn-outline-secondary"),
        ],
        "annual-maintenance-contracts": [
            ("Request Proposal", "contact", "btn-brand"),
            ("Schedule Inspection", "contact", "btn-outline-brand"),
        ],
        "smart-factory-consulting": [
            ("Book Factory Audit", "contact", "btn-brand"),
            ("Automation Strategy", "contact", "btn-outline-brand"),
            ("Budget Planning", "contact", "btn-outline-secondary"),
        ],
    }
    cta_list = service_ctas.get(service.slug, [
        ("Enquire About This Service", "contact", "btn-brand"),
    ])
    return render(request, "services/detail.html", {"service": service, "service_ctas": cta_list})


# --- Blog -----------------------------------------------------------------
def blog_list(request):
    posts = get_published_posts()
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categories = get_all_categories()
    featured = posts.filter(is_featured=True).first()
    return render(request, "blog/list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "featured_post": featured,
    })


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects.select_related("category", "author").filter(
            published_at__lte=timezone.now()
        ),
        slug=slug,
    )
    recent = get_published_posts().exclude(slug=slug)[:5]
    return render(request, "blog/detail.html", {"post": post, "recent_posts": recent})


# --- Content pages --------------------------------------------------------
def faq(request):
    general_faqs = get_faqs_by_category(FAQ.Category.GENERAL)
    service_faqs = get_faqs_by_category(FAQ.Category.SERVICE)
    return render(request, "content/faq.html", {
        "general_faqs": general_faqs,
        "service_faqs": service_faqs,
    })


def gallery(request):
    items = GalleryItem.objects.all().order_by("category", "order")
    items_by_cat = defaultdict(list)
    for item in items:
        items_by_cat[item.category or "Uncategorized"].append(item)
    return render(request, "content/gallery.html", {"items_by_cat": dict(items_by_cat)})


def awards(request):
    return render(request, "content/awards.html", {"awards": get_all_awards()})


def downloads(request):
    items = Download.objects.all().order_by("-created_at")
    downloads_by_type = defaultdict(list)
    for item in items:
        downloads_by_type[item.get_type_display()].append(item)
    return render(request, "content/downloads.html", {"downloads_by_type": dict(downloads_by_type)})


def contact(request):
    return render(request, "contact/contact.html")


# --- Careers --------------------------------------------------------------
def careers_list(request):
    from apps.careers.models import JobOpening

    openings = JobOpening.objects.filter(is_open=True)
    return render(request, "careers/list.html", {"openings": openings})


def career_detail(request, slug):
    from apps.careers.models import JobOpening

    opening = get_object_or_404(JobOpening, slug=slug, is_open=True)
    return render(request, "careers/detail.html", {"opening": opening})


def robots_txt(request):
    """Serve a minimal robots.txt pointing at the sitemap."""
    host = request.get_host()
    scheme = request.scheme
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Allow: /",
        f"Sitemap: {scheme}://{host}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# --- Error handlers -------------------------------------------------------
def handler400(request, exception=None):
    return render(request, "400.html", status=400)


def handler403(request, exception=None):
    return render(request, "403.html", status=403)


def handler404(request, exception=None):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)