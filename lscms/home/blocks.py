# home/blocks.py
from wagtail import blocks
import requests

class APIContentBlock(blocks.StructBlock):
    """Block for fetching and displaying content from an API endpoint."""
    api_url = blocks.URLBlock(help_text="Enter the API endpoint URL")
    template = blocks.CharBlock(
        default="blocks/api_content.html", 
        help_text="Template to render the API content"
    )
    
    class Meta:
        icon = 'site'
        template = 'blocks/api_content.html'
        label = "API Content"
 