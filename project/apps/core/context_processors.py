from django.conf import settings
from django.templatetags.static import static


def _resolve(url: str) -> str:
    """Allow either a full URL/absolute path or a static file path."""
    if url and not (url.startswith("http") or url.startswith("/")):
        return static(url)
    return url


def global_settings(request):
    return {
        "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
        "GOOGLE_ANALYTICS_ID": getattr(settings, "GOOGLE_ANALYTICS_ID", ""),
        "HERO_VIDEO_URL": _resolve(getattr(settings, "HERO_VIDEO_URL", "")),
        "HERO_VIDEO_POSTER": _resolve(getattr(settings, "HERO_VIDEO_POSTER", "")),
    }
