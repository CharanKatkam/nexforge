"""Root URL configuration: Django admin, the DRF API, SEO, and template pages."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.defaults import page_not_found, server_error
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from apps.accounts.views import obtain_auth_token
from apps.blog.views import BlogViewSet
from apps.careers.views import JobApplicationViewSet, JobOpeningViewSet
from apps.contact.views import EnquiryViewSet
from apps.content.views import (
    AwardViewSet,
    DownloadViewSet,
    FAQViewSet,
    GalleryItemViewSet,
    TestimonialViewSet,
)
from apps.core import views as core_views
from apps.core.sitemaps import SITEMAPS
from apps.projects.views import ProjectViewSet
from apps.services.views import ServiceViewSet

# Custom error handlers
handler400 = "apps.core.views.handler400"
handler403 = "apps.core.views.handler403"
handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("services", ServiceViewSet, basename="service")
router.register("blog", BlogViewSet, basename="blog")
router.register("enquiries", EnquiryViewSet, basename="enquiry")
router.register("faqs", FAQViewSet, basename="faq")
router.register("gallery", GalleryItemViewSet, basename="galleryitem")
router.register("awards", AwardViewSet, basename="award")
router.register("downloads", DownloadViewSet, basename="download")
router.register("testimonials", TestimonialViewSet, basename="testimonial")
router.register("jobs", JobOpeningViewSet, basename="job")
router.register("applications", JobApplicationViewSet, basename="application")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/login/", obtain_auth_token, name="api-login"),
    # drf-spectacular API docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": SITEMAPS},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", core_views.robots_txt, name="robots"),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Error page preview in dev
    urlpatterns += [
        path("404/", page_not_found, {"exception": Exception("Page not found")}),
        path("500/", server_error),
    ]
    # django-debug-toolbar (enabled in dev settings) needs its own URLs,
    # otherwise its template reverses the unregistered 'djdt' namespace.
    try:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    except ImportError:
        pass