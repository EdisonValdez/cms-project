# lscms/lscms/models.py

from django.db import models 
from wagtail.models import Page
from wagtail.fields import RichTextField   
from django.db import models
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField 
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock, ChoiceBlock

class HeaderBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True)  
    
    panels = [
        FieldPanel('title'),
        FieldPanel('content'),
    ]
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Header Block"
        verbose_name_plural = "Header Blocks"

class FooterBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = RichTextField(blank=True)   
    
    panels = [
        FieldPanel('content'),
    ]
    
    def __str__(self):
        return f"Footer Block {self.id}"
    
    class Meta:
        verbose_name = "Footer Block"
        verbose_name_plural = "Footer Blocks"

class AdBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, default="Advertisement")  
    image = models.ImageField(upload_to='ads/')
    link = models.URLField()
    
    panels = [  
        FieldPanel('title'),
        FieldPanel('image'),
        FieldPanel('link')
    ]
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Ad Block"
        verbose_name_plural = "Ad Blocks"

class SEOSettings(models.Model):
    title = models.CharField(max_length=60)  # Optimal SEO title length
    meta_description = models.CharField(max_length=160)  # Optimal meta description length
    meta_keywords = models.CharField(max_length=200)
    og_title = models.CharField(max_length=60, blank=True)
    og_description = models.CharField(max_length=200, blank=True)
    og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    canonical_url = models.URLField(blank=True)
    robots_settings = models.CharField(
        max_length=50,
        choices=[
            ('index,follow', 'Index and Follow'),
            ('noindex,follow', 'No Index but Follow'),
            ('index,nofollow', 'Index but No Follow'),
            ('noindex,nofollow', 'No Index and No Follow'),
        ],
        default='index,follow'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('meta_description'),
        FieldPanel('meta_keywords'),
        FieldPanel('robots_settings'),
        FieldPanel('og_title'),
        FieldPanel('og_description'),
        FieldPanel('og_image'),
        FieldPanel('canonical_url'),
    ]

    class Meta:
        verbose_name = 'SEO Setting'
        verbose_name_plural = 'SEO Settings'

    def __str__(self):
        return self.title
 
class MenuItem(models.Model):
    title = models.CharField(max_length=50)
    link_url = models.CharField(max_length=500)
    icon = models.CharField(max_length=50, blank=True)
    sort_order = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    platform_visibility = ArrayField(
        models.CharField(max_length=20),
        default=list,  # Changed from default=list(['web', 'ios', 'android'])
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.platform_visibility:
            self.platform_visibility = ['web', 'ios', 'android']

class CampaignContentBlock(StructBlock):
    title = CharBlock(required=True, help_text="Content block title")
    content_type = ChoiceBlock(choices=[
        ('banner', 'Banner'),
        ('popup', 'Popup'),
        ('sidebar', 'Sidebar'),
        ('embedded', 'Embedded Content')
    ], required=True)
    content = RichTextBlock(required=True)
    call_to_action = CharBlock(required=False)
    button_text = CharBlock(required=False)
    link_url = CharBlock(required=False)
    
    class Meta:
        template = 'blocks/campaign_content_block.html'
 
class MarketingCampaign(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    target_platforms = ArrayField(
        models.CharField(max_length=20),
        default=list,
        blank=True
    )
    target_locations = ArrayField(
        models.CharField(max_length=100),
        default=list,
        blank=True
    )
    priority = models.IntegerField(default=0)
   
    # Updated JSONField imports
    style_settings = JSONField(
        default=dict,
        blank=True,
        help_text="Custom styling options for the campaign"
    )
   
    analytics_tracking = JSONField(
        default=dict,
        blank=True,
        help_text="Analytics tracking configuration"
    )

    campaign_settings = JSONField(
        default=dict,
        blank=True,
        help_text="Campaign display and tracking settings"
    )
    
    # Add the missing field that you're trying to access in __init__
    campaign_content = JSONField(
        default=dict,
        blank=True,
        help_text="Campaign content blocks and metadata"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.target_platforms:
            self.target_platforms = ['web', 'ios', 'android']
        if not self.campaign_content:
            self.campaign_content = {
                'blocks': [],
                'metadata': {}
            }
        if not self.campaign_settings:
            self.campaign_settings = {
                'display': {
                    'type': 'banner',
                    'position': 'top',
                    'style': {}
                },
                'tracking': {
                    'enabled': False,
                    'events': []
                }
            }
            
class NotificationMessage(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=[
            ('info', 'Information'),
            ('success', 'Success'),
            ('warning', 'Warning'),
            ('error', 'Error'),
        ]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    target_platforms = ArrayField(
        models.CharField(max_length=20),
        default=list,  # Changed from default=list(['web', 'ios', 'android'])
        blank=True
    )
    is_dismissible = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.target_platforms:
            self.target_platforms = ['web', 'ios', 'android']
 
class LayoutSettings(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(
        max_length=20,
        choices=[('web', 'Web'), ('ios', 'iOS'), ('android', 'Android')]
    )
    header_style = models.CharField(max_length=50)
    footer_style = models.CharField(max_length=50)
    sidebar_enabled = models.BooleanField(default=True)
    navigation_style = models.CharField(max_length=50)
    color_scheme = JSONField(
        default=dict,
        blank=True,
        help_text="Color scheme configuration"
    )
    custom_css = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('platform'),
        FieldPanel('header_style'),
        FieldPanel('footer_style'),
        FieldPanel('sidebar_enabled'),
        FieldPanel('navigation_style'),
        FieldPanel('color_scheme'),
        FieldPanel('custom_css'),
    ]

class AnalyticsSettings(models.Model):
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    custom_scripts = models.TextField(blank=True)
    enable_tracking = models.BooleanField(default=True)
    privacy_policy_url = models.URLField(blank=True)
    cookie_consent_required = models.BooleanField(default=True)

    panels = [
        FieldPanel('google_analytics_id'),
        FieldPanel('facebook_pixel_id'),
        FieldPanel('custom_scripts'),
        FieldPanel('enable_tracking'),
        FieldPanel('privacy_policy_url'),
        FieldPanel('cookie_consent_required'),
    ]
 