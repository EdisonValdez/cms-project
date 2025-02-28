from django import template
from ..models import ThemeSettings

register = template.Library()

@register.simple_tag
def get_theme_logo():
    """Return the custom logo if set."""
    try:
        theme_settings = ThemeSettings.objects.first()
        if theme_settings and theme_settings.logo:
            return theme_settings.logo
    except Exception:
        pass
    return None
