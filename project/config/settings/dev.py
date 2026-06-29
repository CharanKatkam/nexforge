"""Development settings."""

from .base import *  # noqa: F401,F403

DEBUG = True

# Use simple static file serving in dev (no manifest needed)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

# Allow the local frontend during development.
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# Print emails to the console instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Debug toolbar
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1", "localhost"]
# Off by default; enable per-session with ?djdt=1 or by flipping SHOW_TOOLBAR.
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: request.GET.get("djdt") == "1",
    "IS_RUNNING_TESTS": False,
}

# CSP report-only in dev — copy the same directives for report-only mode
CONTENT_SECURITY_POLICY_REPORT_ONLY = CONTENT_SECURITY_POLICY.copy()