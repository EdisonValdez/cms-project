from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/custom_admin.css')
    )

@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    # Customize menu items if needed
    menu_items[:] = [item for item in menu_items if item.name != 'snippets']

@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/custom_admin.css')
    )

# Custom welcome text
@hooks.register('construct_homepage_panels')
def add_custom_panel(request, panels):
    from wagtail.admin.ui.components import Component
    
    class WelcomePanel(Component):
        template_name = 'wagtailadmin/welcome_panel.html'
        
        def get_context_data(self, parent_context):
            return {
                'request': parent_context['request'],
            }
    
    panels.append(WelcomePanel())
