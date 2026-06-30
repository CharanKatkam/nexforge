"""Sitemaps for SEO."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.projects.models import Project
from apps.services.models import Service


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return ["home", "projects-portfolio", "services-list", "blog-list",
                "contact", "about", "faq", "careers-list"]

    def location(self, item):
        return reverse(item)


class CareerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        from apps.careers.models import JobOpening
        return JobOpening.objects.filter(is_open=True)

    def location(self, obj):
        return reverse("career-detail", args=[obj.slug])


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("project-detail", args=[obj.slug])


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("service-detail", args=[obj.slug])


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(published_at__lte=timezone.now())

    def lastmod(self, obj):
        return obj.published_at

    def location(self, obj):
        return reverse("blog-detail", args=[obj.slug])


SITEMAPS = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
    "services": ServiceSitemap,
    "blog": BlogSitemap,
    "careers": CareerSitemap,
}
