# home/models.py
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

class HTMLBlock(blocks.RawHTMLBlock):
    """HTML block for adding raw HTML content."""
    class Meta:
        icon = "code"
        label = "HTML"

class StandardPage(Page):
    """
    A standard page with a flexible content area.
    """
    intro = models.CharField(max_length=250, blank=True)
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('html', HTMLBlock()),
        ('embed', EmbedBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('card', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('text', blocks.TextBlock()),
            ('image', ImageChooserBlock(required=False)),
            ('button_text', blocks.CharBlock(required=False)),
            ('button_link', blocks.URLBlock(required=False)),
        ])),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
 
class HomePage(Page):
    """
    Home page model with a flexible content area.
    """
    banner_title = models.CharField(max_length=100, blank=True)
    banner_subtitle = models.CharField(max_length=250, blank=True)
    
    content = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('html', HTMLBlock()),
        ('embed', EmbedBlock()),
        ('featured_sections', blocks.ListBlock(
            blocks.StructBlock([
                ('title', blocks.CharBlock()),
                ('text', blocks.TextBlock()),
                ('image', ImageChooserBlock(required=False)),
                ('link', blocks.URLBlock(required=False)),
            ])
        )),
        # Add APIContentBlock if needed later
    ], use_json_field=True, blank=True)
    
    edit_handler = TabbedInterface([
        ObjectList([
            FieldPanel('banner_title'),
            FieldPanel('banner_subtitle'),
        ], heading='Banner'),
        ObjectList([
            FieldPanel('content'),
        ], heading='Content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'),
    ])
    