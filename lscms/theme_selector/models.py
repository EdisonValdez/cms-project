# theme_selector/models.py
# theme_settings/models.py
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

@register_setting
class ThemeSettings(BaseSiteSetting):
    """Settings for admin theme customization."""
    
    COLOR_THEMES = (
        ('default', 'Default (Blue)'),
        ('green', 'Green Theme'),
        ('purple', 'Purple Theme'),
        ('red', 'Red Theme'),
        ('teal', 'Teal Theme'),
        ('custom', 'Custom Colors'),
    )
    
    theme = models.CharField(
        max_length=20,
        choices=COLOR_THEMES,
        default='default',
        help_text='Select the color theme for the admin interface'
    )
    
    custom_primary_color = models.CharField(
        max_length=7,
        blank=True,
        help_text='Custom primary color (hex code, e.g., #FF5733)'
    )
    
    custom_secondary_color = models.CharField(
        max_length=7,
        blank=True,
        help_text='Custom secondary color (hex code, e.g., #33FF57)'
    )
    
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Custom logo for the admin interface'
    )
    
    custom_css = models.TextField(
        blank=True,
        help_text='Additional CSS to be applied to the admin interface'
    )
    
    panels = [
        FieldPanel('theme'),
        FieldPanel('custom_primary_color'),
        FieldPanel('custom_secondary_color'),
        FieldPanel('logo'),
        FieldPanel('custom_css'),
    ]
    
    class Meta:
        verbose_name = 'Admin Theme'
