"""Base settings shared across all environments.

Environment-specific overrides live in ``dev.py`` and ``prod.py``. Secrets and
deployment-varying values are read from the environment via ``django-environ``.
"""

from pathlib import Path

import dj_database_url
import environ
from csp.constants import NONCE

# config/settings/base.py -> config/settings -> config -> project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# django-environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["127.0.0.1", "localhost"]),
    EMAIL_PORT=(int, 587),
    EMAIL_USE_TLS=(bool, True),
    CORS_ALLOWED_ORIGINS=(list, []),
    CSP_REPORT_ONLY=(bool, True),
)

# Read .env file if it exists
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Third party
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "csp",
    # Local apps
    "apps.core",
    "apps.projects",
    "apps.services",
    "apps.blog",
    "apps.contact",
    "apps.content",
    "apps.accounts",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.global_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": dj_database_url.parse(env("DATABASE_URL"), conn_max_age=600),
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 9,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "60/min",
        "user": "240/min",
        "enquiry": "5/min",
        "auth": "10/min",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Email
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_USE_TLS = env("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@nexforgeautomation.com")
SALES_INBOX = env("SALES_INBOX", default="sales@nexforgeautomation.com")
GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY", default="")
# Google Analytics 4 Measurement ID (e.g. G-XXXXXXXXXX). Empty = analytics off.
GOOGLE_ANALYTICS_ID = env("GOOGLE_ANALYTICS_ID", default="")
# Hero background video. Empty = animated SVG/grid only (no video).
# Use a static path ("video/hero.mp4") or a full https URL (add its host to CSP media-src).
HERO_VIDEO_URL = env("HERO_VIDEO_URL", default="")
HERO_VIDEO_POSTER = env("HERO_VIDEO_POSTER", default="")

# drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "NexForge Automation API",
    "DESCRIPTION": "Industrial automation services and projects API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/v1",
    "CONTACT": {"name": "NexForge Automation", "email": "info@nexforgeautomation.com"},
    "LICENSE": {"name": "Proprietary"},
    "ENUM_NAME_OVERRIDES": {
        "ProjectStatusEnum": "apps.projects.models.Project.Status",
        "EnquiryStatusEnum": "apps.contact.models.Enquiry.Status",
    },
}

# CSP (django-csp 4.0+) - allowlist for production
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": [NONCE, "'self'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://www.googletagmanager.com"],
        # 'unsafe-inline' kept for style only: the templates use inline style="" attributes,
        # which a nonce cannot cover. Style attributes cannot execute scripts, so XSS risk is
        # low; script-src stays strict (nonce + allowlist, no inline).
        "style-src": ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com", "https://fonts.googleapis.com"],
        "font-src": ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
        "img-src": ["'self'", "data:", "https:"],
        # Hero video: 'self' covers a local static file. To use an external video host,
        # add it here (e.g. "https://cdn.coverr.co", "https://videos.pexels.com").
        "media-src": ["'self'", "data:"],
        "connect-src": ["'self'", "https://www.google-analytics.com", "https://region1.google-analytics.com"],
        "frame-src": ["https://www.google.com"],
        "object-src": ["'none'"],
        "base-uri": ["'self'"],
        "form-action": ["'self'"],
        "frame-ancestors": ["'none'"],
    },
}
CONTENT_SECURITY_POLICY_REPORT_ONLY = env("CSP_REPORT_ONLY")