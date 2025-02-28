# In lscms/management/commands/copy_wagtail_static.py
import os
import shutil
from pathlib import Path
import site

from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Copy Wagtail admin static files to the static directory'

    def handle(self, *args, **options):
        # Get the site-packages directory where wagtail is installed
        site_packages = site.getsitepackages()[0]
        wagtail_admin_static = Path(site_packages) / "wagtail" / "admin" / "static" / "wagtailadmin"
        
        # Create the static directory if it doesn't exist
        static_dir = Path(settings.STATIC_ROOT) / "wagtailadmin"
        if not static_dir.exists():
            os.makedirs(static_dir, exist_ok=True)
            
        self.stdout.write(f"Copying Wagtail admin static files from {wagtail_admin_static} to {static_dir}")
        
        # Copy all files recursively
        for root, dirs, files in os.walk(wagtail_admin_static):
            for file in files:
                src = Path(root) / file
                rel_path = src.relative_to(wagtail_admin_static)
                dst = static_dir / rel_path
                
                # Create parent directories if needed
                os.makedirs(dst.parent, exist_ok=True)
                
                # Copy the file
                shutil.copy2(src, dst)
                
        self.stdout.write(self.style.SUCCESS('Successfully copied Wagtail admin static files'))

# python manage.py copy_wagtail_static
