# theme_selector/wagtail_hooks.py
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks

from .utils import darken_hex_color, lighten_hex_color
from .models import ThemeSettings

@hooks.register('insert_global_admin_css')
def global_theme_css():
    """Add theme CSS to the Wagtail admin."""
    # Try to get the theme settings
    try:
        theme_settings = ThemeSettings.objects.first()
        if not theme_settings:
            # Return default if no settings found
            return format_html(
                '<link rel="stylesheet" href="{}">',
                static('css/admin-themes/default.css')
            )
            
        theme = theme_settings.theme
        
        # Handle custom theme
        if theme == 'custom' and theme_settings.custom_primary_color:
            # Generate inline CSS for custom colors
            primary = theme_settings.custom_primary_color
            secondary = theme_settings.custom_secondary_color or primary
            
            return format_html(
                '<style>'
                ':root {{'
                '  --w-color-primary: {primary};'
                '  --w-color-primary-200: {primary_light};'
                '  --w-color-primary-400: {primary};'
                '  --w-color-primary-600: {primary_dark};'
                '  --w-color-primary-800: {primary_darker};'
                '  --w-color-secondary: {secondary};'
                '  --w-color-secondary-100: {secondary_light};'
                '  --w-color-secondary-400: {secondary};'
                '  --w-color-secondary-600: {secondary_dark};'
                '}}'
                '.sidebar {{'
                '  background-color: {primary_darker};'
                '}}'
                '.sidebar__inner .nav-main a:hover,'
                '.sidebar__inner .nav-main a.sidebar-menu-item--active {{'
                '  background-color: {primary_dark};'
                '}}'
                '.button-primary {{'
                '  background-color: var(--w-color-primary);'
                '  border-color: var(--w-color-primary-600);'
                '}}'
                '.button-primary:hover {{'
                '  background-color: var(--w-color-primary-600);'
                '}}'
                '{custom_css}'
                '</style>',
                primary=primary,
                primary_light=lighten_hex_color(primary, 20),
                primary_dark=darken_hex_color(primary, 10),
                primary_darker=darken_hex_color(primary, 20),
                secondary=secondary,
                secondary_light=lighten_hex_color(secondary, 20),
                secondary_dark=darken_hex_color(secondary, 10),
                custom_css=theme_settings.custom_css,
            )
        else:
            # Return the predefined theme CSS
            css_output = format_html(
                '<link rel="stylesheet" href="{}">',
                static(f'css/admin-themes/{theme}.css')
            )
            
            # Add custom CSS if specified
            if theme_settings.custom_css:
                css_output += format_html(
                    '<style>{}</style>',
                    theme_settings.custom_css
                )
                
            return css_output
            
    except Exception as e:
        # Fallback to default in case of any errors
        return format_html(
            '<link rel="stylesheet" href="{}">',
            static('css/admin-themes/default.css')
        )

@hooks.register('insert_global_admin_js')
def global_admin_js():
    """Add custom JavaScript for admin theme features."""
    return format_html(
        '<script>'
        'document.addEventListener("DOMContentLoaded", function() {{'
        '  console.log("Admin theme applied successfully");'
        '}});'
        '</script>'
    )

# Optional: Customize the logo if uploaded
@hooks.register('construct_main_menu')
def customize_logo(request, menu_items):
    try:
        theme_settings = ThemeSettings.objects.first()
        if theme_settings and theme_settings.logo:
            # This is a placeholder - actual logo replacement would need template overrides
            pass
    except Exception:
        pass