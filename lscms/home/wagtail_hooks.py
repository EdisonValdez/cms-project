# home/wagtail_hooks.py
from wagtail import hooks
from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML
from django.templatetags.static import static
from django.utils.html import format_html
 
@hooks.register('insert_global_admin_css')
def global_admin_css():
    """Add custom CSS to the Wagtail admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">\n',
        static('CACHE/css/wagtail_admin.css')
    )
 
# First, make sure DOM is properly initialized
html_exporter = HTML()

@hooks.register('register_rich_text_features')
def register_code_feature(features):
    """Adds the code block feature to the rich text editor."""
    feature_name = 'code'
    type_ = 'CODE'

    control = {
        'type': type_,
        'label': '</>',
        'description': 'Code',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    # Fixed version of the converter rule
    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'pre[class=code]': lambda el: {'type': type_}},
        'to_database_format': {'element': 'pre', 'props': {'class': 'code'}},
    })

    features.default_features.append(feature_name)
