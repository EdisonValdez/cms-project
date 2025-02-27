# LSOperations/lscms/lscms/wsgi.py

import os
import sys
from pathlib import Path

# Get the absolute path to the project root
file_path = Path(__file__).resolve()
project_root = file_path.parent.parent.parent  # Go up three levels: lscms/lscms -> lscms -> LSOperations

# Add the project root to the Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lscms.settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
