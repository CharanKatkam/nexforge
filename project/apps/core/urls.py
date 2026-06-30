"""Template page routes."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("projects/", views.projects_portfolio, name="projects-portfolio"),
    path("projects/<slug:slug>/", views.project_detail, name="project-detail"),
    path("services/", views.services_list, name="services-list"),
    path("services/<slug:slug>/", views.service_detail, name="service-detail"),
    path("blog/", views.blog_list, name="blog-list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog-detail"),
    path("faq/", views.faq, name="faq"),
    path("gallery/", views.gallery, name="gallery"),
    path("awards/", views.awards, name="awards"),
    path("downloads/", views.downloads, name="downloads"),
    path("contact/", views.contact, name="contact"),
    path("careers/", views.careers_list, name="careers-list"),
    path("careers/<slug:slug>/", views.career_detail, name="career-detail"),
]
