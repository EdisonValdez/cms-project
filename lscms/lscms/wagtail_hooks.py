# lscms/lscms/wagtail_hooks.py
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from home.models import HomePage 
from wagtail_modeladmin.options import (
    ModelAdmin, 
    ModelAdminGroup, 
    modeladmin_register
)
from .models import (
    SEOSettings, 
    HeaderBlock, 
    FooterBlock, 
    AdBlock, 
    MenuItem, 
    MarketingCampaign, 
    NotificationMessage, 
    LayoutSettings, 
    AnalyticsSettings
)
# icon from https://wagtail.org/design/icon-library/

 
class SEOSettingsAdmin(ModelAdmin):
    model = SEOSettings
    menu_label = 'SEO Settings'
    menu_icon = 'site'
    menu_order = 10
    add_to_settings_menu = False   
    list_display = ('title', 'meta_description',  'meta_keywords', 'og_title', 'og_description', 'canonical_url', 'robots_settings')
    search_fields = ('title', 'meta_description', 'meta_keywords', 'og_title', 'og_description', 'canonical_url')
    list_filter = ('robots_settings',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

class MenuItemAdmin(ModelAdmin):
    model = MenuItem
    menu_label = 'Navigation Menu'
    menu_icon = 'list-ul'
    menu_order = 300
    list_display = ('title', 'link_url', 'sort_order', 'is_active')
    search_fields = ('title', 'link_url')
    list_filter = ('is_active', 'platform_visibility')
    ordering = ('sort_order',)

class MarketingCampaignAdmin(ModelAdmin):
    model = MarketingCampaign
    menu_label = 'Marketing Campaigns'
    menu_icon = 'pick'
    menu_order = 400
    list_display = ('name', 'start_date', 'end_date', 'is_active', 'priority')
    search_fields = ('name',)
    list_filter = ('is_active', 'target_platforms')
    ordering = ('-start_date',)

class NotificationMessageAdmin(ModelAdmin):
    model = NotificationMessage
    menu_label = 'Notifications'
    menu_icon = 'warning'
    menu_order = 500
    list_display = ('title', 'type', 'start_date', 'end_date', 'priority')
    search_fields = ('title', 'message')
    list_filter = ('type', 'is_dismissible', 'target_platforms')
    ordering = ('-priority', '-start_date')

class LayoutSettingsAdmin(ModelAdmin):
    model = LayoutSettings
    menu_label = 'Layout Settings'
    menu_icon = 'desktop'
    menu_order = 600
    list_display = ('name', 'platform', 'header_style', 'footer_style')
    search_fields = ('name',)
    list_filter = ('platform', 'sidebar_enabled')

class AnalyticsSettingsAdmin(ModelAdmin):
    model = AnalyticsSettings
    menu_label = 'Analytics'
    menu_icon = 'time'
    menu_order = 700
    list_display = ('google_analytics_id', 'facebook_pixel_id', 'enable_tracking')
    list_filter = ('enable_tracking', 'cookie_consent_required')

class HeaderBlockAdmin(ModelAdmin):
    model = HeaderBlock
    menu_label = 'Header Blocks'
    menu_icon = 'title'
    menu_order = 200
    list_display = ('title', 'content')
    search_fields = ('title', 'content')

class FooterBlockAdmin(ModelAdmin):
    model = FooterBlock
    menu_label = 'Footer Blocks'
    menu_icon = 'key'
    menu_order = 300
    list_display = ('id', 'content')
    search_fields = ('content',)

class AdBlockAdmin(ModelAdmin):
    model = AdBlock
    menu_label = 'Ad Blocks'
    menu_icon = 'list-ul'
    menu_order = 400
    list_display = ('title', 'link')
    search_fields = ('title',)

# Register each admin individually
modeladmin_register(HeaderBlockAdmin)
modeladmin_register(FooterBlockAdmin)
modeladmin_register(AdBlockAdmin)

class HomePageAdmin(ModelAdmin):
    model = HomePage
    menu_label = 'Home Pages'
    menu_icon = 'home'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'intro')
    search_fields = ('title', 'intro')
 
class ContentManagementGroup(ModelAdminGroup):
    menu_label = 'Content Management'
    menu_icon = 'folder-open-inverse'
    menu_order = 200
    items = (
        MenuItemAdmin,
        MarketingCampaignAdmin,
        NotificationMessageAdmin,
    )

class WebSettingsGroup(ModelAdminGroup):
    menu_label = 'Site Settings'
    menu_icon = 'cogs'
    menu_order = 300
    items = (
        SEOSettingsAdmin,
        LayoutSettingsAdmin,
        AnalyticsSettingsAdmin,
    )

class PagesGroup(ModelAdminGroup):
    menu_label = 'Pages'
    menu_icon = 'doc-full'
    menu_order = 400
    items = (
        HomePageAdmin,
    )

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">\n'
        '<style>'
        '.wagtail-logo {{'
        '  width: auto;'
        '  height: 40px;'  # Adjust height as needed
        '  margin: 0.3em;'
        '}}'
        '</style>',
        static('css/custom_admin.css')
    )

@hooks.register('construct_main_menu')
def customize_main_menu(request, menu_items):
    """Customize main menu items if needed"""
    pass

@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/custom_admin.css')
    )
 
 
modeladmin_register(ContentManagementGroup)
modeladmin_register(WebSettingsGroup)
modeladmin_register(PagesGroup)
modeladmin_register(SEOSettingsAdmin)
 


"""
modeladmin_register(HomePageAdmin)
modeladmin_register(HeaderBlockAdmin)
modeladmin_register(FooterBlockAdmin)
modeladmin_register(AdBlockAdmin)"""
